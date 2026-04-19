"""
One-off cleanup: delete every Bluesky post the runner has ever made,
and clear the matching `distribution_logs` rows so they're eligible
for re-posting on the next cron.

Why we have this:
    The first generation of posts went out as "title + naked URL +
    hashtags" — robotic, AI-bot energy. After switching to the
    `social_hook + rich link card` format we want a clean slate so the
    feed first impression matches the new voice. This script makes
    that switchover one command instead of five clicks.

Usage:
    # On Render (web shell or cron shell — both have BLUESKY_* env):
    python scripts/delete_bluesky_posts.py

    # Locally:
    BLUESKY_HANDLE=... BLUESKY_APP_PASSWORD=... DATABASE_URL=... \
        python scripts/delete_bluesky_posts.py

    # Add --dry-run to see what *would* be deleted without touching
    # anything in Bluesky or the database.
"""

from __future__ import annotations

import argparse
import logging
import re
import sys

from src.distribution import bluesky
from src.distribution.runner import CHANNEL_BLUESKY
from src.models import DistributionLog, SessionLocal, init_db


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("delete_bluesky_posts")


_RKEY_RE = re.compile(r"/post/([A-Za-z0-9]+)")


def _extract_rkey(value: str | None) -> str | None:
    """Pull the rkey out of a stored bsky.app post URL."""
    if not value:
        return None
    m = _RKEY_RE.search(value)
    return m.group(1) if m else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without making any changes.",
    )
    args = parser.parse_args()

    if not bluesky.is_enabled():
        logger.error("Bluesky credentials not configured (BLUESKY_HANDLE / BLUESKY_APP_PASSWORD)")
        return 2

    init_db()
    db = SessionLocal()
    try:
        rows = (
            db.query(DistributionLog)
            .filter(DistributionLog.channel == CHANNEL_BLUESKY)
            .filter(DistributionLog.success.is_(True))
            .order_by(DistributionLog.created_at.asc())
            .all()
        )
        if not rows:
            logger.info("No bluesky distribution_logs rows to clean up. Nothing to do.")
            return 0

        logger.info("Found %d bluesky post row(s) to delete.", len(rows))

        client = bluesky.get_client() if not args.dry_run else None
        if client is not None and not client.ensure_session():
            logger.error("Bluesky login failed; aborting.")
            return 3

        deleted_posts = 0
        skipped_no_rkey = 0
        deleted_log_rows = 0
        delete_failed = 0

        for row in rows:
            rkey = _extract_rkey(row.response_snippet)
            if rkey is None:
                logger.warning(
                    "row id=%s: no rkey in response_snippet=%r — leaving Bluesky post alone, "
                    "but will still drop the log row so it's re-eligible.",
                    row.id, row.response_snippet,
                )
                skipped_no_rkey += 1
            else:
                if args.dry_run:
                    logger.info("[dry-run] would delete bluesky rkey=%s (url=%s)", rkey, row.url)
                else:
                    ok = client.delete_post(rkey)
                    if ok:
                        deleted_posts += 1
                    else:
                        delete_failed += 1
                        logger.warning("Failed to delete rkey=%s; keeping log row so we can retry.", rkey)
                        continue

            if args.dry_run:
                logger.info("[dry-run] would drop distribution_logs row id=%s", row.id)
            else:
                db.delete(row)
                deleted_log_rows += 1

        if not args.dry_run:
            db.commit()

        logger.info(
            "Done. deleted_posts=%d delete_failed=%d log_rows_dropped=%d skipped_no_rkey=%d",
            deleted_posts, delete_failed, deleted_log_rows, skipped_no_rkey,
        )
        return 0 if delete_failed == 0 else 1
    except Exception as exc:
        logger.exception("Cleanup failed: %s", exc)
        try:
            db.rollback()
        except Exception:
            pass
        return 4
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
