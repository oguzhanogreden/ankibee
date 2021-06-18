from PyQt5 import QtGui
from PyQt5 import QtWidgets
from beetime.goal_table_model import GoalTableModel
import json
import os
from anki.decks import DeckManager

from aqt import mw
from aqt.qt import *
from requests.models import HTTPError
from beetime.config_layout import Ui_BeeminderSettings
from PyQt5.QtWidgets import QDialog

from .api import get_user
from .data_service import DataService

class BeeminderSettings(QDialog):
    """Create a settings menu."""

    def __init__(self):
        super().__init__()

        self.ui = Ui_BeeminderSettings()
        self.ui.setupUi(self)

        self.ui.buttonBox.rejected.connect(self.on_reject)
        self.ui.buttonBox.accepted.connect(self.on_accept)

        # self.ui.added_deck_selector.currentIndexChanged.connect(self.on_added_deck_selector_change)
        
        self.check_credentials_and_redirect()

        self._set_fields()
        
        dataService = DataService(self.read_config())
        tableModel = GoalTableModel(parent=None, data=dataService.to_nested_list())
        self.ui.goals_table.setModel(tableModel)
        # Columns should expand to fill width
        self.ui.goals_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        
    def check_credentials_and_redirect(self):
        config = self.read_config()
        
        try:
            get_user(config["username"], config["token"])
            self.ui.tabWidget.setCurrentIndex(1)
        except HTTPError as e:
            self.ui.enabled.setChecked(False)
            
    def _set_fields(self):
        config = self.read_config()
        
        print(config["added"][0])

        self.ui.username.setText(config["username"])
        self.ui.token.setText(config["token"])
        self.ui.enabled.setChecked(config["enabled"])
        self.ui.shutdown.setChecked(config["shutdown"])
        self.ui.ankiweb.setChecked(config["ankiweb"])

        # self.ui.time_units.setCurrentIndex(config["time"]["units"])

        # self.ui.time_slug.setText(config["time"]["slug"])
        # self.ui.time_enabled.setChecked(config["time"]["enabled"])
        # self.ui.time_premium.setChecked(config["time"]["premium"])
        # self.ui.time_agg.setCurrentIndex(config["time"]["agg"])

        # self.ui.reviewed_slug.setText(config["reviewed"]["slug"])
        # self.ui.reviewed_enabled.setChecked(config["reviewed"]["enabled"])
        # self.ui.reviewed_premium.setChecked(config["reviewed"]["premium"])
        # self.ui.reviewed_agg.setCurrentIndex(config["reviewed"]["agg"])

        # added = self.get_added_at_index(config, "added", 0)
        # self.load_added_data(added)

        
    def get_added_at_index(self, config, goal_type:str ,index: int) -> dict:
        return config[goal_type][index]
        
    def load_added_data(self, added: dict) -> None:
        self.ui.added_type.setCurrentIndex(added["type"])
        self.ui.added_slug.setText(added["slug"])
        self.ui.added_enabled.setChecked(added["enabled"])
        self.ui.added_premium.setChecked(added["premium"])
        self.ui.added_agg.setCurrentIndex(added["agg"])
        

    def on_reject(self):
        self.close()

    def on_accept(self):
        self.on_apply()
        self.close()

    def on_apply(self):
        previous = self.read_config()

        config = {
            "added": {
                "agg": self.ui.added_agg.currentIndex(),
                "enabled": self.ui.added_enabled.isChecked(),
                "overwrite": self.set_overwrite(
                    previous["added"]["premium"], previous["added"]["agg"]
                ),
                "premium": self.ui.added_premium.isChecked(),
                "slug": self.ui.added_slug.text(),
                "type": self.ui.added_type.currentIndex(),
            },
            "ankiweb": self.ui.ankiweb.isChecked(),
            "enabled": self.ui.enabled.isChecked(),
            "shutdown": self.ui.shutdown.isChecked(),
            "reviewed": {
                "agg": self.ui.reviewed_agg.currentIndex(),
                "enabled": self.ui.reviewed_enabled.isChecked(),
                "premium": self.ui.reviewed_premium.isChecked(),
                "overwrite": self.set_overwrite(
                    previous["reviewed"]["premium"], previous["reviewed"]["agg"]
                ),
                "slug": self.ui.reviewed_slug.text(),
            },
            "time": {
                "agg": self.ui.time_agg.currentIndex(),
                "enabled": self.ui.time_enabled.isChecked(),
                "overwrite": self.set_overwrite(
                    previous["time"]["premium"], previous["time"]["agg"]
                ),
                "premium": self.ui.time_premium.isChecked(),
                "slug": self.ui.time_slug.text(),
                "units": self.ui.time_units.currentIndex(),
            },
            "token": self.ui.token.text(),
            "username": self.ui.username.text(),
        }
        self.write(config)

    def on_added_deck_selector_change(self, index: int):
        config = self.read_config()
        
        added = self.get_added_at_index(config, "added", index)

        # deck name may have changed
        deck_name = self.get_deck_name_for_id(added["deckId"])
        self.ui.added_deck_selector.setEditText(deck_name)
        
        self.load_added_data(added)

    @classmethod
    def read_config(cls):
        return mw.addonManager.getConfig(__name__)

    @classmethod
    def write(cls, config):
        mw.addonManager.writeConfig(__name__, config)

    @staticmethod
    def set_overwrite(premium, agg):
        return not premium or (premium and agg == 0)

    @staticmethod
    def get_deck_name_for_id(id: int) -> str:
        deck_manager = DeckManager(mw.col)
        
        return deck_manager.name(id, default=True)
