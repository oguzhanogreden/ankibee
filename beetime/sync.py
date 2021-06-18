import datetime

from aqt import mw
from beetime.lookup import format_comment, lookup_added, lookup_reviewed
from beetime.config import BeeminderSettings

from .beeminder_client import prepare_api_call
from .constants import TRACKED_OBJECT_NAMES

NOON = 12
SECONDS_PER_MINUTE = 60

def sync_dispatch(col=None, at=None):
    """Tally the time spent reviewing and send it to Beeminder.

    Based on code by: muflax <mail@muflax.com>, 2012
    """

    col = col or mw.col
    if col is None:
        return

    config = BeeminderSettings.read_config()

    try:
        if (
            at == "shutdown"
            and not config["shutdown"]
            or at == "ankiweb"
            and not config["ankiweb"]
            or not config["enabled"]
        ):
            return
    except:
        raise RuntimeError(config)

    mw.progress.start(immediate=True)
    mw.progress.update("Syncing with Beeminder...")

    deadline = datetime.datetime.fromtimestamp(col.sched.dayCutoff).hour
    now = datetime.datetime.today()

    # upload all datapoints with an artificial time of 12 pm (noon)
    report_dt = datetime.datetime(now.year, now.month, now.day, NOON)
    if now.hour < deadline:
        report_dt -= datetime.timedelta(days=1)
    report_ts = report_dt.timestamp()

    if is_enabled("time") or is_enabled("reviewed"):
        n_cards, review_time = lookup_reviewed(col)
        comment = format_comment(n_cards, review_time)

        if is_enabled("time"):
            units = config["time"]["units"]
            while units < 2:
                review_time /= SECONDS_PER_MINUTE
                units += 1
            prepare_api_call(col, report_ts, review_time, comment)

        if is_enabled("reviewed"):
            prepare_api_call(col, report_ts, n_cards, comment, goal_type="reviewed")

    for index, added in enumerate(config["added"]):
        if added["enabled"]:
            type_ = TRACKED_OBJECT_NAMES[added["type"]]
            # todo: pass down deck id
            n_added = lookup_added(col, type_)
            print(n_added)
            prepare_api_call(
                col, report_ts, n_added, f"added {n_added} {type_}", goal_type="added", index=index
            )

    mw.progress.finish()


def is_enabled(goal):
    # goal here is either:
    # - review time
    # - number of reviews
    # - number of additions
    return BeeminderSettings.read_config()[goal]["enabled"]
