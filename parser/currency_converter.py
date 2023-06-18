amd = "AMD"
us = "US"
cad = "CA"
eur = "€"
usd_amd = 389
cad_amd = 291
eur_amd = 423
exchange = {
    amd: {
        amd: 1,
        us: 1 / usd_amd,
        cad: 1 / cad_amd,
        eur: 1 / eur_amd,
    },
    us: {
        amd: usd_amd,
        us: 1,
        cad: usd_amd / cad_amd,
        eur: usd_amd / eur_amd
    },
    cad: {
        amd: cad_amd,
        us: cad_amd / usd_amd,
        cad: 1,
        eur: cad_amd / eur_amd
    }

}


class CurrencyBucket(dict):
    def to_currency(self, currency: str) -> float:
        total = 0
        for curr, value in self.items():
            total += value * exchange[curr][currency]
        return total
