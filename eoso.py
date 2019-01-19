import os.path
import re
import pyodbc
import random
import cherrypy

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Compounding Data Base.mdb;')
cursor = conn.cursor()

formatting = '''
                    <head>
                    <title>Electronic Oso Adjustment Calculator</title>
                    
                    <style>
                        .main {
                            text-align: center;
                            width: 500px;
                            border: 25px solid lightgrey;
                            border-radius: 5px;
                            padding: 25px;
                            margin: 25px;
                            }
                        .docheading {
                            text-align: left;
                            font-family: DejaVu Sans Mono, monospace;
                            text-indent: 30px;
                            }
                        #home {
                            background: linear-gradient(
                            to top,
                            rgba(255,255,255,1) 80%,
                            rgba(255,255,255,0)),
                            url("static/bgimg.png");
                            }
                        h1  {
                            color: grey;
                            font-family: DejaVu Sans Mono, monospace;
                            text-shadow: 3px 2px green;
                            }
                        p, ul   {
                            text-align: left;
                            font-family: helvetica, sans-serif;
                            }
                        .console {
                            font-family: DejaVu Sans Mono, monospace;
                            }
                        #options {
                            display: none;
                            }
                        #optionsbutton {
                            text-align:left;
                            }
                        #documentationbutton {
                            text-align:left;
                            }
                        .typewriter {
                            font-size: 14px;
                            font-family: DejaVu Sans Mono, monospace;
                            overflow: hidden;
                            border-right: .15em solid transparent;
                            white-space: nowrap;
                            margin: 0 auto;
                            letter-spacing: .15em;
                            animation: 
                                typing 4s steps(30, end),
                                blink-caret .88s step-end 4;
                            }
                        @keyframes typing {
                            from { width: 0 }
                            to { width: 100% }
                            }
                        @keyframes blink-caret {
                            from, to { border-color: transparent }
                            50% { border-color: green; }
                            }
                            
                    </style
                    </head>
                    '''


class WelcomePage:

    @cherrypy.expose
    def index(self):

        cursor.execute("SELECT [Lot Number] FROM [CMP Spec Table]")
        dbcounter = []

        for row in cursor.fetchall():
            dbcounter.append(re.search(r"(\s|[a-zA-Z0-9].*[a-zA-Z0-9])", str(row)).group(0))

        dbcount = str(len(dbcounter))
        

        return formatting + '''

            <body>
            <div class="main" id="home">
            <h1>Electronic Oso</h1>
            <a href="randomoso"><img src="static/Oso.png" width="450" height="124"></a>
            <hr><h3 class="typewriter">{''' + dbcount + ''' records currently in the picnic basket}</h3><hr>
            <form action="eoso" method="GET">
            <p style=\"text-indent: 40px\">Enter a part ID: <input type="text" name="isort" placeholder="Required" /></p>
            <p style=\"text-indent: 40px\">Enter a pH value: <input type="number" step="0.01" name="iph" placeholder="Leave blank to skip" /></p>
            <p style=\"text-indent: 40px\">Enter a viscosity value: <input type="number" name="ivisc" placeholder="Leave blank to skip" /></p>
            <p style=\"text-indent: 40px\">Enter a sample size (g): <input type="number" name="isample_size" placeholder="Leave blank to skip" /></p>
            <p style=\"text-indent: 40px\">Enter a batch size (Kg): <input type="number" name="isize" placeholder="Required" /></p>
            <div style="text-align:center"><input type="submit" /></div>
            <hr>
            <div style="text-align:left;">
            <button id="documentationbutton" type="button" name="Documentation" onclick="location.href='documentation'">Documentation</button>
            <button id="optionsbutton" type="button" name="Options" onclick="showhideOptions()">Advanced</button>
            </div>
            <br>
            <div id="options" style="font-family: DejaVu Sans Mono, monospace; text-align:left">
            <input type="checkbox" name="option1" value="verbose">Show data table<br><br>
            <input type="checkbox" name="option2" value="detector">Anomaly detection (beta)<br><br>
            Record Interval:<input style="width:80px;" type="number" name="startinterval" /> to <input style="width:80px;" type="number" name="endinterval" />
            </div>
            </form>
            </div>
            <script>
                    function showhideOptions() {
                        var x = document.getElementById("options");
                        if (x.style.display === "block") {
                            x.style.display = "none";
                        } else {
                            x.style.display = "block";
                        }
                    }
            </script>
            </body>
            '''
    
    @cherrypy.expose
    def randomoso(self):
        batchsizes = [650, 1250, 1650, 3300, 3500]
        url = "/eoso?isort=EVE0" + str(random.randint(1, 34)) + "&iph=" + str(random.randint(400, 700)/100) + "&ivisc=" + str(random.randint(400, 4000)) + "&isample_size=" + str(random.randint(200, 600)) + "&isize=" + str(batchsizes[random.randint(0, 4)])
        raise cherrypy.HTTPRedirect(url) 
    
    @cherrypy.expose
    def documentation(self):
        return formatting + '''
                <body>
                <div class="main">
                <h1>Documentation</h1>
                <hr>
                <div>
                <h2 class="docheading"><a style="color:black;" href="javascript:showhidedoc('usage');">Usage</a></h2>
                <div id="usage" style="padding:5px 15px; border-radius:5px; background-color:lightgrey; display:none;">
                <p>Complete the form and press submit. Part ID and batch size are required, the other fields may be left blank if they are not relevant. A report will be created preceded by any notes regarding script execution. Record count is updated in realtime and information on advanced options can be viewed in the next section.</p>
                <p>Poke the bear to generate a random query.</p>
                </div>
                <h2 class="docheading"><a style="color:black;" href="javascript:showhidedoc('advanced');">Advanced Options</a></h2>
                <div id="advanced" style="padding:5px 15px; border-radius:5px; background-color:lightgrey; display:none;">
                <ul>
                <li><strong>Data Table:</strong> selecting this option will append a table showing information about each record scanned.</li>
                <br>
                <li><strong>Anomaly Detection:</strong> (usable but work in progress) selecting this option will compare ph and viscosity to the average initial ph and average initial viscosity of the scanned records.</li>
                <br>
                <li><strong>Record Interval:</strong> inclusive and specified using batch record numbers, this provides a further data filter.</li>
                </ul>
                </div>
                <h2 class="docheading"><a style="color:black;" href="javascript:showhidedoc('work');">How does E-Oso work?</a></h2>
                <div id="work" style="padding:5px 15px; border-radius:5px; background-color:lightgrey; display:none">
                <p style=\"text-indent: 40px\">Database records are first filtered by matching the product Part ID and batch size with records that have adjustments. Records with nonstandard adjustments, overadjustments, or two adjustments are ignored. The remaining adjustments are used to calculate the average percent chemical required to increase or decrease a specification by one unit, the specific adjustment percent. The input specifications are then compared against target specifications which are generated by averaging the release specifications of the records. The specific adjustment percent is multiplied by the difference between input and target specifications and then by the batch size to produce a result.</p>
                </div>
                <h2 class="docheading"><a style="color:black;" href="javascript:showhidedoc('advlim');">Advantages and Limitations</a></h2>
                <div id="advlim" style="padding:5px 15px; border-radius:5px; background-color:lightgrey; display:none;">
                <p style=\"text-indent: 40px\">This tool provides a rapid assessment for typical batches and is capable of making correct adjustment suggestions for both pH and viscosity. The largest advantage is that the calculation uses data recorded from the end results of production scale tank adjustments. This is important because the accuracy of the adjustment suggestion is driven by the consistency of the data and allows any sources of error characterizing the data to be implicit in the suggestion.</p>
                <p style=\"text-indent: 40px\">The main limitation is a consequence of the simplicity of the calculation, which models the formula of a line passing through the origin of a graph. The model does not take into account certain nuances such as the adjustment of one specification effecting the other specification also. To improve consistency, and as a result accuracy, the data is filtered to only examine typical batches but in doing so this constrains the suggestion to only be valuable and applicable to a typical batch. The advanced option <i>Anomaly Detector</i> is an early attempt at putting in place a system of comparators for determining batch regularity. Ideally, batch regularity would be represented by a continuous value as an indicator for adjustment suggestion success chance.</p>
                </div>
                </div>
                <hr>
                <p><a href="./">Done</a></p>
                </div>
                <script>
                    function showhidedoc(docid) {
                        var x = document.getElementById(docid);
                        if (x.style.display === "block") {
                            x.style.display = "none";
                        } else {
                            x.style.display = "block";
                        }
                    }
                </script>
                </body>
            '''


    @cherrypy.expose
    def eoso(self, isort=None, iph=None, ivisc=None, isample_size=None, isize=None, startinterval=None, endinterval=None, option1=None, option2=None):


        isort = isort.upper()

        if isort:
            sort = isort
        else:
            return formatting + '<div class="main"><img src="static/troyoso.png"><p class="console">Part ID required, click <a href="./">here</a> to try again.</p></div>'

        if isize:
            size = isize
        else:
            return formatting + '<div class="main"><img src="static/troyoso.png"><p class="console">Batch size required, click <a href="./">here</a> to try again.</p></div>'



        tableheaders = ["Lot Number", "Part Number", "Start Date", "Batch Size Kg", "Specific Gravity Final", "Viscosity Intial", "Viscosity Final", "pH (10% solution) Intial", "pH (10% solution) Final", "Comments"]
        tabledata = []

        batch_ph = []
        batch_viscosity = []
        release_ph = []
        release_viscosity = []
        chm007_ph_factors = []
        chm146_ph_factors = []
        chm125_viscosity_factors = []
        chm188_viscosity_factors = []
        run_params = []
        report = []

        class Batch:
            def __init__(self, batch_number, part_id, date, size, specific_gravity, initial_viscosity, final_viscosity, initial_ph, final_ph, comments):
                self.batch_number = int(batch_number)
                self.part_id = part_id
                self.date = date
                try:
                    self.size = float(size)
                except:
                    self.size = -1
                try:
                    self.specific_gravity = float(specific_gravity)
                except:
                    self.specific_gravity = -1
                try:
                    initial_viscosity = initial_viscosity.replace(',', '')
                    self.initial_viscosity = float(initial_viscosity)
                except:
                    self.initial_viscosity = -1
                try:
                    final_viscosity = final_viscosity.replace(',', '')
                    self.final_viscosity = float(final_viscosity)
                except:
                    self.final_viscosity = -1
                try:
                    self.initial_ph = float(initial_ph)
                except:
                    self.initial_ph = -1
                try:
                    self.final_ph = float(final_ph)
                except:
                    self.final_ph = -1
                self.adjustment_string = comments

            def gather_release_specs(self):
                if self.final_viscosity != -1:
                    release_viscosity.append(self.final_viscosity)
                if self.final_ph != -1:
                    release_ph.append(self.final_ph)

            def gather_batch_specs(self):
                if self.initial_viscosity != -1:
                    batch_viscosity.append(self.initial_viscosity)
                if self.initial_ph != -1:
                    batch_ph.append(self.initial_ph)


            def gather_adjustments(self):
                if self.adjustment_string != "None":
                    if re.search("CHM125", self.adjustment_string, re.IGNORECASE) and re.search("CHM188", self.adjustment_string, re.IGNORECASE):
                        #print("counter viscosity adjustment")
                        return
                    if re.search("CHM007", self.adjustment_string, re.IGNORECASE) and re.search("CHM146", self.adjustment_string, re.IGNORECASE):
                        #print("counter ph adjustment")
                        return
                    double_check = ["CHM007", "CHM146", "CHM125", "CHM188"]
                    for item in double_check:
                        count = self.adjustment_string.upper().count(item)
                        if count > 1:
                            #print("double adjustment")
                            return
                    if re.search("CHM015", self.adjustment_string, re.IGNORECASE) or re.search("CHM031", self.adjustment_string, re.IGNORECASE):
                        #print("abnormal adjustment")
                        return

                    adjustments = re.findall(r"([0123456789.]+(?:\s|)(?:KG|G)\sCHM\d\d\d)", self.adjustment_string, re.IGNORECASE) #works but maybe [0123456789.] should maybe have \.
                    for adjustment in adjustments:

                        chm = re.search("CHM...", adjustment).group(0)
                        chm.upper()

                        try:
                            amt = float(re.search(r"[0-9\.]+", adjustment).group(0))
                            if re.search("KG|G", adjustment, re.IGNORECASE).group(0) in ["g", "G"]:
                                amt = amt / 1000
                        except:
                            #print("fail at float amt")
                            continue

                        if chm == "CHM188":
                            if self.initial_viscosity != -1 and self.final_viscosity != -1 and self.initial_viscosity != self.final_viscosity:
                                chm188_viscosity_factors.append(amt / self.size / (self.final_viscosity - self.initial_viscosity))
                                #print("chm188")

                        elif chm == "CHM125":
                            if self.initial_viscosity != -1 and self.final_viscosity != -1 and self.initial_viscosity != self.final_viscosity:
                                chm125_viscosity_factors.append(amt / self.size / (self.final_viscosity - self.initial_viscosity))
                                #print("chm125")

                        if chm == "CHM007":
                            if self.initial_ph  != -1 and self.final_ph != -1 and self.initial_ph != self.final_ph:
                                chm007_ph_factors.append(amt / self.size / (self.final_ph - self.initial_ph))
                                #print("chm007")

                        elif chm == "CHM146":
                            if self.initial_ph != -1 and self.final_ph != -1 and self.initial_ph != self.final_ph:
                                chm146_ph_factors.append(amt / self.size / (self.final_ph - self.initial_ph))
                                #print("chm146")







        def compute_ph_adjustment(current_ph, average_release_ph, batch_size, sample_size):
            if average_release_ph == -1:
                run_params.append("<p class=\"console\">Error calculating release pH...</p>")
                return
            elif current_ph > average_release_ph:
                if len(chm007_ph_factors) != 0:
                    chm007_amount = str(round(abs((current_ph - average_release_ph) * sum(chm007_ph_factors) / len(chm007_ph_factors) * batch_size), 2))
                    chm007_percent = round(float(chm007_amount) / batch_size * 100, 2)
                    if chm007_percent > 2.5:
                        report.append("<p>Add " + chm007_amount + "KG CHM007 <font color=\"red\">(" + str(chm007_percent) + "%)</font>, based on " + str(len(chm007_ph_factors)) + " adjustments</p>")
                    else:
                        report.append("<p>Add " + chm007_amount + "KG CHM007 (" + str(chm007_percent) + "%), based on " + str(len(chm007_ph_factors)) + " adjustments</p>")

                    if sample_size != "":
                        report.append("<p style=\"text-indent: 40px\"><i>Try adding " + str(round(abs((current_ph - average_release_ph) * sum(chm007_ph_factors) / len(chm007_ph_factors) * sample_size), 2)) + "g CHM007 to your sample</i></p>")
                else:
                    report.append("<p>No CHM007 adjustments found...</p>")
            elif current_ph < average_release_ph:
                if len(chm146_ph_factors) != 0:
                    chm146_amount = str(round(abs((average_release_ph - current_ph) * sum(chm146_ph_factors) / len(chm146_ph_factors) * batch_size), 2))
                    chm146_percent = round(float(chm146_amount) / batch_size * 100, 2)
                    if chm146_percent > 2.5:
                        report.append("<p>Add " + chm146_amount + "KG CHM146 <font color=\"red\">(" + str(chm146_percent) + "%)</font>, based on " + str(len(chm146_ph_factors)) + " adjustments</p>")
                    else:
                        report.append("<p>Add " + chm146_amount + "KG CHM146 (" + str(chm146_percent) + "%), based on " + str(len(chm146_ph_factors)) + " adjustments</p>")
                    if sample_size != "":
                        report.append("<p style=\"text-indent: 40px\"><i>Try adding " + str(round(abs((current_ph - average_release_ph) * sum(chm146_ph_factors) / len(chm146_ph_factors) * sample_size), 2)) + "g CHM146 to your sample</i></p>")
                else:
                    report.append("<p>No CHM146 adjustments found...</p>")

        def compute_viscosity_adjustment(current_viscosity, average_release_viscosity, batch_size, sample_size):
            if average_release_viscosity == -1:
                run_params.append("<p class=\"console\">Error calculating release viscosity...</p>")
                return
            elif current_viscosity > average_release_viscosity:
                if len(chm188_viscosity_factors) != 0:
                    chm188_amount = str(round(abs((current_viscosity - average_release_viscosity) * sum(chm188_viscosity_factors) / len(chm188_viscosity_factors) * batch_size), 2))
                    chm188_percent = round(float(chm188_amount) / batch_size * 100, 2)
                    if chm188_percent > 2.5:
                        report.append("<p>Add " + chm188_amount + "KG CHM188 <font color=\"red\">(" + str(chm188_percent) + "%)</font>, based on " + str(len(chm188_viscosity_factors)) + " adjustments</p>")
                    else:
                        report.append("<p>Add " + chm188_amount + "KG CHM188 (" + str(chm188_percent) + "%), based on " + str(len(chm188_viscosity_factors)) + " adjustments</p>")
                    if sample_size != "":
                        report.append("<p style=\"text-indent: 40px\"><i>Try adding " + str(round(abs((current_viscosity - average_release_viscosity) * sum(chm188_viscosity_factors) / len(chm188_viscosity_factors) * sample_size), 2)) + "g CHM188 to your sample</i></p>")
                else:
                    report.append("<p>No CHM188 adjustments found...</p>")
            elif current_viscosity < average_release_viscosity:
                if len(chm125_viscosity_factors) != 0:
                    chm125_amount = str(round(abs((average_release_viscosity - current_viscosity) * sum(chm125_viscosity_factors) / len(chm125_viscosity_factors) * batch_size), 2))
                    chm125_percent = round(float(chm125_amount) / batch_size * 100, 2)
                    if chm125_percent > 2.5:
                        report.append("<p>Add " + chm125_amount + "KG CHM125 <font color=\"red\">(" + str(chm125_percent) + "%)</font>, based on " + str(len(chm125_viscosity_factors)) + " adjustments</p>")
                    else:
                        report.append("<p>Add " + chm125_amount + "KG CHM125 (" + str(chm125_percent) + "%), based on " + str(len(chm125_viscosity_factors)) + " adjustments</p>")
                    if sample_size != "":
                        report.append("<p style=\"text-indent: 40px\"><i>Try adding " + str(round(abs((current_viscosity - average_release_viscosity) * sum(chm125_viscosity_factors) / len(chm125_viscosity_factors) * sample_size), 2)) + "g CHM125 to your sample</i></p>")
                else:
                    report.append("<p>No CHM125 adjustments found...</p>")






        for item in tableheaders:
             cursor.execute("SELECT [" + item + "] FROM [CMP Spec Table]")
             column = []

             for row in cursor.fetchall():
                column.append(re.search(r"(\s|[a-zA-Z0-9].*[a-zA-Z0-9])", str(row)).group(0)) #changed group1 to group0

             tabledata.append(column)

        db_size = len(tabledata[0])

        while True:#legacy from original script, probably don't need in web version



            sort = isort
            try:
                ph = float(iph)
            except:
                ph = ""
                run_params.append("<p class=\"console\">pH not entered... pH skipped</p>")
            try:
                visc = float(ivisc)
            except:
                visc = ""
                run_params.append("<p class=\"console\">viscosity not entered... viscosity skipped</p>")
            try:
                sample_size = float(isample_size)
            except:
                sample_size = ""
                run_params.append("<p class=\"console\">sample size not entered... validation suggestion skipped</p>")
            try:
                size = float(isize)
            except:
                #print("Batch size required!")
                continue
            dataselect = [[] for _ in range(10)]

            if startinterval != None and startinterval != '':
                start_interval = startinterval
                run_params.append("<p class=\"console\">Start interval set to: " + start_interval + "</p>")
            else:
                start_interval = 0
            
            if endinterval != None and endinterval !='':
                end_interval = endinterval
                run_params.append("<p class=\"console\">End interval set to: " + end_interval + "</p>")
            else:
                end_interval = 999999





            for row in tabledata[0]:
                if tabledata[1][tabledata[0].index(row)] == sort and str(tabledata[3][tabledata[0].index(row)]) == str(size) and int(start_interval) <= int(tabledata[0][tabledata[0].index(row)]) <= int(end_interval):
                    for index in range(10):
                        dataselect[index].append(tabledata[index][tabledata[0].index(row)])

            if len(dataselect[0]) <= 5: #bug where batches with filtered out adjustments prevent this from triggering, suggest checking len(adjustments) in gather_adjustments() for > 0
                run_params.append("<p class=\"console\">5 or less records found for specified batch size... running computation for all batch sizes</p>")
                for row in tabledata[0]:
                    if tabledata[1][tabledata[0].index(row)] == sort and int(tabledata[0][tabledata[0].index(row)]):
                        for index in range(10):
                            dataselect[index].append(tabledata[index][tabledata[0].index(row)])
                if len(dataselect[0]) == 0:
                        return formatting + '''
                                <div class="main">
                                <img src="static/troyoso.png"><br>
                                <p class="console">No batches found... click <a href="./">here</a> to try again.</p>
                                </div>
                               '''


            for i in [3, 5, 6]: #may not need this anymore with current class init
                for row in dataselect[i]:
                    row = row.replace(',', '')
                    row = row.replace('\s', '')
                    row = row.lstrip()
                    row = row.rstrip()



            for row in dataselect[0]:
                batch = Batch(dataselect[0][dataselect[0].index(row)], dataselect[1][dataselect[0].index(row)], dataselect[2][dataselect[0].index(row)], dataselect[3][dataselect[0].index(row)], dataselect[4][dataselect[0].index(row)], dataselect[5][dataselect[0].index(row)], dataselect[6][dataselect[0].index(row)], dataselect[7][dataselect[0].index(row)], dataselect[8][dataselect[0].index(row)], dataselect[9][dataselect[0].index(row)])
                batch.gather_adjustments()
                batch.gather_release_specs()
                batch.gather_batch_specs()


            if len(release_ph) != 0:
                average_release_ph = sum(release_ph) / len(release_ph)
            else:
                average_release_ph = -1
            if len(release_viscosity) != 0:
                average_release_viscosity = sum(release_viscosity) / len(release_viscosity)
            else:
                average_release_viscosity = -1
                


            report.append("<p><b>Complete!</b></p>")
            report.append("<p>Scanned " + str(len(dataselect[0])) + " records...</p>")
            report.append("<br><p><b>Input Parameters:</b></p>")
            report.append("<p>Part ID: " + str(sort) + "</p>")
            report.append("<p>pH value: " + str(ph) + "</p>")
            report.append("<p>Viscosity value: " + str(visc) + "</p>")
            report.append("<p>Sample size (g): " + str(sample_size) + "</p>")
            report.append("<p>Batch size (Kg): " + str(size) + "</p><br>")
            

            
            if visc != "" and average_release_viscosity != -1:
                report.insert(2, "<p style=\"text-indent: 40px\">Target release viscosity: " + str(round(average_release_viscosity, 2)) + "</p>")
            if ph != "" and average_release_ph != -1:
                report.insert(2, "<p style=\"text-indent: 40px\">Target release pH: " + str(round(average_release_ph, 2)) + "</p>")
            report.append("<br><p><b>Computed adjustments:</b></p>")
            if ph != "":
                compute_ph_adjustment(ph, average_release_ph, size, sample_size)
                #print()
            if visc != "":
                compute_viscosity_adjustment(visc, average_release_viscosity, size, sample_size)
                #print()

            table_data = ""
            if option1 == "verbose":
                table_data = '<hr><table style="text-align:center; width:100%"><tr><th>Batch #</th><th>Size</th><th>Initial Visc</th><th>Final Visc</th><th>Initial pH</th><th>Final pH</th><th>Adjustment</th></tr>'
                for row in dataselect[0]:
                    table_row = "<tr>"
                    for index in [0, 3, 5, 6, 7, 8, 9]:
                        table_row = table_row + "<td>" + str(dataselect[index][dataselect[0].index(row)]) + "</td>"
                    table_row = table_row + "</tr>"
                    table_data = table_data + table_row
                table_data = table_data + "</table>"

            detector_string = ""
            if option2 == "detector":
                detector_string = "<p class=\"console\">Anomaly detection complete...</p>"
                if len(batch_ph) != 0:
                    average_batch_ph = round(sum(batch_ph) / len(batch_ph), 2)
                    if ph != "":
                        if float(ph) < (average_batch_ph * 0.65) or float(ph) > (average_batch_ph * 1.35):
                            detector_string = detector_string + "<p class=\"console\" style=\"color:red\">Abnormal pH, average initial pH is " + str(average_batch_ph) + "</p>"
                        else:
                            detector_string = detector_string + "<p class=\"console\">pH normal.</p>"
                else:
                    detector_string = detector_string + "<p class=\"console\">pH detection error!</p>"
                if len(batch_viscosity) != 0:
                    average_batch_viscosity = round(sum(batch_viscosity) / len(batch_viscosity), 2)
                    if visc != "":
                        if float(visc) < (average_batch_viscosity * 0.65) or float(visc) > (average_batch_viscosity * 1.35):
                            detector_string = detector_string + "<p class=\"console\" style=\"color:red\">Abnormal viscosity, average initial viscosity is " + str(average_batch_viscosity) + "</p>"
                        else:
                            detector_string = detector_string + "<p class=\"console\">Viscosity normal.</p>"
                else:
                    detector_string = detector_string + "<p class=\"console\">Viscosity detection error!</p>"
                run_params.append(detector_string)

            final_result_string = ""

            for i in run_params:
                final_result_string = final_result_string + i
                
            if run_params != []:
                final_result_string = final_result_string + "<hr>"

            for i in report:
                final_result_string = final_result_string + i

            final_result_string = formatting + "<div class=\"main\"><img src=\"static/result.png\"><hr>" + final_result_string + "<hr><p><a href=\"./\">Done</a></p>" + table_data + "</div>"

            

            return final_result_string

            break



current_dir = os.path.dirname(os.path.abspath(__file__)) + os.path.sep

global_conf = {
       'global':    { 'server.environment': 'production',
                      'engine.autoreload_on': True,
                      'engine.autoreload_frequency': 5,
                      'server.socket_host': '0.0.0.0',
                      'server.socket_port': 80,
                    },
            '/':{
                    'tools.staticdir.root' : current_dir,
            },
            '/static':{
                'tools.staticdir.on' : True,
                'tools.staticdir.dir' : 'static',
            },
       }


if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().

    cherrypy.quickstart(WelcomePage(), config=global_conf)

