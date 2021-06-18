from anki.collection import Collection
from anki.decks import Deck, DeckManager
from beetime.exceptions import LastUploadIsNotSetException
from anki.lang import ngettext
from anki.utils import fmtTimeSpan
from beetime.config import BeeminderSettings
from beetime.util import get_day_stamp

def get_data_point_id(goal_type, timestamp, index=None):
    """ Compare the cached dayStamp with the current one, return
    a tuple with as the first item the cached datapoint ID if
    the dayStamps match, otherwise None; the second item is
    a boolean indicating whether they match (and thus if we need
    to save the new ID and dayStamp.
    Disregard mention of the second item in the tuple.
    """
    config = BeeminderSettings.read_config()
    
    day_stamp = get_day_stamp(timestamp)
    
    goal_data = config[goal_type]
    
    if index is not None:
        goal_data = goal_data[0]
    
    try:
        if goal_data["overwrite"] and _lastupload_equals(goal_data["lastupload"], day_stamp):
            return goal_data["did"]
    except LastUploadIsNotSetException:
        # lastupload isn't set.
        # hypothesis: this happens on first run
        return None

        
def _lastupload_equals(last_upload, day_stamp: str) -> bool:
    try:
        return last_upload == day_stamp 
    except KeyError:
        raise LastUploadIsNotSetException


def format_comment(n_cards, review_time):

    msgp1 = ngettext("%d card", "%d cards", n_cards) % n_cards
    return _(f"studied {msgp1} in {fmtTimeSpan(review_time, unit=1)}")


def lookup_reviewed(col):
    """Lookup the number of cards reviewed and the time spent reviewing them."""
    cardsReviewed, reviewTime = col.db.first(
        "select count(), sum(time)/1000 from revlog where id > ?",
        (col.sched.dayCutoff - 86400) * 1000,
    )
    return (cardsReviewed or 0, reviewTime or 0)


def lookup_added(col: Collection, type_="cards") -> int:
    deck_manager = DeckManager(col)

    deck_id = deck_manager.id_for_name("The Deck")
    
    
    if deck_id is None:
        raise Exception
    
    print(deck_id)

    if type_ == "cards":
        return col.db.scalar(
            """select count() from {type_} 
            where id > {id_}
            and (
                did = {deck_id}
                or odid = {deck_id}
            )""".format(type_=type_, id_=(col.sched.dayCutoff - 86400) * 1000, deck_id=deck_id)
    )
    elif type_ == "notes":
        return col.db.scalar(
            """select count(distinct notes.id) from notes 
            left join cards
            on notes.id = cards.nid
            where notes.id > {id_}
            and (
                cards.did = {deck_id}
                or cards.odid = {deck_id}
            )""".format(id_=(col.sched.dayCutoff - 86400) * 1000, deck_id=deck_id)
        )
    else:
        # argumentexception?
        raise Exception
