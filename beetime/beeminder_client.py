from beetime.api import send_datapoints_of_goal
from beetime.lookup import get_data_point_id
from beetime.config import BeeminderSettings
from beetime.util import get_day_stamp



def prepare_api_call(col, timestamp, value, comment, goal_type="time", index=None):
    """Prepare the API call to beeminder.

    Based on code by: muflax <mail@muflax.com>, 2012
    """
    config = BeeminderSettings.read_config()
    user = config["username"]
    token = config["token"]
    
    goal_data = config[goal_type]
    
    # TODO: This needs to go once the config is modeled better, these operations are abstracted.
    if index is not None:
        goal_data = goal_data[index]

    slug = goal_data["slug"]
    data = {
        "timestamp": timestamp,
        "value": value,
        "comment": comment,
        "auth_token": token,
    }

    cached_data_point_id = get_data_point_id(goal_type, timestamp, index=index)

    goal_data["lastupload"] = get_day_stamp(timestamp)
    goal_data["did"] = send_datapoints_of_goal(user, token, slug, data, cached_data_point_id)
    BeeminderSettings.write(config)
    col.setMod()