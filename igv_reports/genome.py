import requests
import json



def get_genome(id):

    genomes_url = "https://igv.org/genomes/genomes.json"
    r = requests.get(genomes_url)

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
