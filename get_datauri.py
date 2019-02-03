from igv_reports import data_uri

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("filename", help="name of file to be converted to data uri")
    parser.add_argument("-t", "--filetype", help="type of file to be converted to data uri")
    parser.add_argument("-r", "--range" , help="genomic range to be converted in the form chr:start-stop")

    args = parser.parse_args()

    uri = data_uri.file_to_data_uri(args.filename, args.filetype, args.range)

    print(uri)