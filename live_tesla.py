import yahoo_fin.stock_info as si
 
tsla = si.get_live_price('tsla')


print(type(tsla))
print(tsla)