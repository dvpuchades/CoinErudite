import util.filler

binance_api_key = 'Cg08zCbyfMWD61glzeRduZ4fNkwcljlEhuy2iLrf2ff6ftivmq4igeEMPwADPWeX'
binance_api_secret = 'aLNxlZIxLLSKvRiiaIy4K2jDjYanEirYZ29cE0Zw2mlxQAkpIhVt14UE0kcRh0qM'

f = filler.filler(binance_api_key, binance_api_secret)

f.minute_generator()