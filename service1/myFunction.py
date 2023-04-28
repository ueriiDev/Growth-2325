import mysql.connector


def enter_period_amount(balance):
    """This is a Python function named enter_period_amount that takes a string as its parameter
    and returns a modified version of the same string. The purpose of this function is to insert
    a decimal point into a string representing a large balance amount."""
    if isinstance(balance, int):
        str_balance = str(balance)
    elif isinstance(balance, str):
        str_balance = balance
    else:
        str_balance = '0'
    if len(str_balance) >= 19:
        str_balance = str_balance[:-18] + "." + str_balance[-18:]
    return str_balance


class Holder:
    """This class represents a holder with a wallet."""

    def __init__(self, id, wallet, token_eth, token_polygon):
        self.id = id
        self.wallet = wallet
        self.token_eth = token_eth
        self.token_polygon = token_polygon

    def update_token_polygon(self, tp):
        self.token_polygon = enter_period_amount(tp)

    def update_token_ethereum(self, te):
        self.token_eth = enter_period_amount(te)


def load_holder(cnx):
    """ Query to retrieve the list of holders """

    query = ("SELECT id, wallet, token_eth, token_polygon FROM holder")
    # Esecuzione della query
    cursor = cnx.cursor()
    cursor.execute(query)
    """ Data retrieval and creation of instances of the Holder class """
    holders = []
    for (id, wallet, token_eth, token_polygon) in cursor:
        holder = Holder(id, wallet, token_eth, token_polygon)
        holders.append(holder)
    return holders


def update_holder(cnx, holder):
    query = ("UPDATE holder SET token_eth = %s, token_polygon = %s WHERE id = %s")
    cursor = cnx.cursor()
    cursor.execute(query, (holder.token_eth, holder.token_polygon, holder.id))
    cnx.commit()


def adjust_token_aggregated(cnx):
    """ Update the aggregated token field """
    query = ("UPDATE holder SET token_aggregated = token_eth + token_polygon")
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
