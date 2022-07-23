amd = "AMD"
us = "US"
cad = "CA"
usd_amd = 499
cad_amd = 387
exchange = {
    amd: {
        amd: 1,
        us: 1 / usd_amd,
        cad: 1 / cad_amd,
    },
    us: {
        amd: usd_amd,
        us: 1,
        cad: usd_amd / cad_amd,
    },
    cad: {
        amd: cad_amd,
        us: cad_amd / usd_amd,
        cad: 1,
    }

}


class CurrencyBucket(dict):
    def to_currency(self, currency: str) -> float:
        total = 0
        for curr, value in self.items():
            total += value * exchange[curr][currency]
        return total
