import requests
import json


def _user_agent():
    """Identify igv-reports when fetching the hosted genome list.

    igv.org filters automated traffic from its usage counters.  Without a
    user agent of our own we are indistinguishable from any other
    python-requests caller, so these fetches cannot be attributed.
    """
    try:
        from importlib.metadata import version   # Python 3.8+
        return "igv-reports/" + version("igv-reports")
    except Exception:
        return "igv-reports"


def get_genome(id):

    genomes_url = "https://igv.org/genomes/genomes3.json"
    r = requests.get(genomes_url, headers={"User-Agent": _user_agent()})

    if r.status_code == 200:
        genomes = r.json()
        genome_ids = []
        for g in genomes:
            if g["id"] == id:
                return g
            genome_ids.append(g["id"])

        # genome not found
        msg = f'Unknown genome ID: {id}. Valid genome values: {", ".join(genome_ids)}'
        raise ValueError(msg)

    else:
        print(f'Error loading genomes {r.status_code}')
        return None



def main():
    genome = get_genome("hg38")
    print (genome)

if __name__ == "__main__":
    main()
