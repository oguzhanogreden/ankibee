import typing
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, QObject, QVariant, Qt

class GoalTableModel(QAbstractTableModel):
	def __init__(self, parent: typing.Optional[QObject], data: typing.List) -> None:
		self.headers = ["Name", "Tracked Objects", "Enabled"]
		self.data = data
		super().__init__(parent=parent)

	def flags(self, index: QModelIndex) -> Qt.ItemFlags:
		# TODO: Checkbox for enabled column
		return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

	def rowCount(self, parent: QModelIndex) -> int:
		return len(self.data)
		
	def columnCount(self, parent: QModelIndex) -> int:
		return len(self.headers)
		
	def data(self, index: QModelIndex, role: int) -> typing.Any:
		if role != Qt.DisplayRole:
			return QVariant()

		return self.data[index.row()][index.column()]
		
	def headerData(self, section: int, orientation: Qt.Orientation, role: int) -> typing.Any:
		if role != Qt.DisplayRole or orientation != Qt.Horizontal:
			return QVariant()

		return self.headers[section]
		
	pass