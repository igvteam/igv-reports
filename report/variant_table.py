import io

class HTMLTable:

    # Always remember the *self* argument
    def __init__(self, vcfFile, headerFile):

        self.header = []
        with open(headerFile, "r") as f:
            data = f.readlines()
            for h in data:
                self.header.append(h.strip('\n\r'))

        self.rows = []

    def addRow(self, row):

        if len(row) != len(self.header):
            raise Exception("Row size != header size")
        self.rows.append(row)



    def __str__(self):

        html = io.StringIO()

        html.write("<table><tr>")
        for h in self.header:
            html.write("<td>")
            html.write(h)
            html.write("</td>")

        for row in self.rows:

            html.write("<tr>")

            for v in row:

                html.write("<td>")
                html.write(v)
                html.write("</td>")

            html.write("</tr>")

        html.write("</table>")

        return html.getvalue()
