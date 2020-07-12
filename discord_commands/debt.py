from debt import Debt
_debt = Debt()

async def cmd_debt(ctx, name: str, name_2 = None, amount = None):
    if name_2 is None:
        debt_owed, debt_owes = _debt.debt_list
        owed_dict = None
        owes_dict = None
        if name in debt_owed:
            owed_dict = debt_owed[name]
        if name in debt_owes:
            owes_dict = debt_owes[name]
        response_str = ""
        if owed_dict is not None:
            response_str += name + " owes:"
            for owed_name in owed_dict.keys():
                response_str += "\n\t" + owed_name + " " + '{:,}gp'.format(owed_dict[owed_name])
        if owes_dict is not None:
            if len(response_str):
                response_str += "\n"
            response_str += name + " is owed:"
            for owes_name in owes_dict.keys():
                response_str += "\n\t" + owes_name + " " + '{:,}gp'.format(owes_dict[owes_name])
        if len(response_str):
            await ctx.send(response_str)
        else:
            await ctx.send(name + " is owed and owes nothing!")
    else:
        _debt.update_debt(name, name_2, amount)
        debt_owed, debt_owes = _debt.debt_list
        owed = 0
        if name in debt_owed:
            if name_2 in debt_owed[name]:
                owed = debt_owed[name][name_2]
        await ctx.send("debt updated, " + name + " now owes " + name_2 + ": " + '{:,}gp'.format(owed))