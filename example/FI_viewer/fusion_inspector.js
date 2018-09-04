var fusionInspectorState = {
  cache : { tabs : [] },
  browserMade : false
}

function loadIGVBrowser( curFusion, curJunctionReads, curSpanningReads, curLeftPos, curRightPos )
{
    // Update header no matter if the browser is being made.
    setFusionDetails( curFusion, curJunctionReads, curSpanningReads );
    // Do not remake browser.
    if( ! fusionInspectorState.browserMade ){

        // Add tab for IGV and click on tab
        $('#tabDescription').append('<li role="presentation" id="igvTab"><a href="#igvDiv" data-toggle="tab">IGV Detail</a></li>')
        $('#tabContent').append('<div role="tabpanel" id="igvDiv" class="tab-pane fade"></div>')
        $('.nav-tabs a[href="#igvDiv]').tab('show');

        // Need a wait to make sure the tabs have switched.
        setTimeout(function(){
            makeIGVBrowser( curFusion );
        }, 1000);

    } else {
        goToFusion( curFusion, curRightPos, curLeftPos );
    }
}

function makeIGVBrowser( curFusion )
{
 $('.nav-tabs a[href="#igvDiv]').tab('show');
}

/**
* Move IGV browser to a fusion of choice by genomic location.
*/
function goToFusion( fusionChr ){ //, fusionBreakRight, fusionBreakLeft ){
    var location = fusionChr
    $('.nav-tabs a[href="#igvDiv"]').tab('show');
    setTimeout(function(){
        fusionInspectorState.cache.curBrowser.search( location );
    }, 1000);
}

/**
 * Update the header information on the page.
 */
function setFusionDetails( fusionName, fusionJunctReads, fusionSpanFrags ){
    $( "#FusionNameDetail" ).html( "<p class='navbar-text'><b>Fusion Name:</b> " + fusionName + "</p>" );
    $( "#FusionJunctionDetail" ).html( "<p class='navbar-text'><b>Junction Read Count:</b> " + fusionJunctReads + "</p>" );
    $( "#FusionSpanningDetail" ).html( "<p class='navbar-text'><b>Spanning Read Count:</b> " + fusionSpanFrags + "</p>" );
}

/**
 * Order the mutation table keys so certain element are in front in a specific order
 * @param {array} ArrayToOrder - Array of elements to reorder.
 * @param {array} forcedOrder - Array of elements that should be at the beginning and in this order.
 */
function orderTableKeysBeginning( arrayToOrder, forcedOrder ){
  newArray = [];
  for( arrayElement = 0; arrayElement < arrayToOrder.length; arrayElement++ ){
    if( !( forcedOrder.indexOf( arrayToOrder[ arrayElement ] ) >= 0 )){
      newArray.push( arrayToOrder[ arrayElement ] );
    }
  }
  return( forcedOrder.concat( newArray ));
}

/**
 * Make a table header row containing a given value.
 * Helper function for the map call.
 * @param {string} tableRowValue - Value to put in the header row.
 */
function toTableRowHeaderElement( tableRowValue ){
    return '<th>' + tableRowValue + '</th>';
}

/**
 * Makes a table row from fusion information, making usre to order the data as given.
 */
function toTableBodyElement( fusionEntry, orderedHeaderKeys ){
  var bodyRow = '<tr>';
  for( var headerKeyIndex = 0; headerKeyIndex < orderedHeaderKeys.length; headerKeyIndex++ ){
    bodyRow = bodyRow + '<td>' + fusionEntry[ orderedHeaderKeys[ headerKeyIndex ] ] + '</td>';
  }
  return( bodyRow + '</tr>');
}

/**
 * Get the annotation info form the data table row.
 */
function getFusionAnnotationFromRow( infoHeader, dataRow ){
  var index = fusionInspectorState.cache.fusionKeys.indexOf( infoHeader );
  if( index == -1 ){
    return( None );
  }
  return( dataRow[ index ] );
}

/**
* Load the fusion list from the json array to a html list
*/
function loadFusionDataTable( ){

    // Forced order of the mutation table elements.
    // Any element in the table and not in this array
    // will be after these elements in the table and will
    // be in no specific order
    var forcedHeaderKeyOrder = ['Fusion', 'Junction Reads', 'Spanning Fragments', 'Splice Type', 'Left Gene', 'Left Chr', 'Left Pos', 'Left Strand', 'Right Gene', 'Right Chr', 'Right Pos', "Right Strand"];

    var fusionKeys = [];
    for( var fusionKey in fusionInspectorState.cache.json.fusions[ 0 ] ){
      if( fusionInspectorState.cache.json.fusions[ 0 ].hasOwnProperty( fusionKey ) ){
        fusionKeys.push( fusionKey );
      }
    }
    // fusionInspectorState.cache[ "fusionKeys" ] = orderTableKeysBeginning( forcedHeaderKeyOrder, fusionKeys );
    // Make data table header and footer
    var fusionTable = $('#fusionTable');
    // var fusionHeader = fusionInspectorState.cache.fusionKeys.map( toTableRowHeaderElement );
    // For loop instead of map
    var fusionHeader = [];
    for (var header = 0; header < forcedHeaderKeyOrder.length; header++){
         fusionHeader.push( '<th>' + forcedHeaderKeyOrder[header] + '</th>');
    }
    fusionTable.append( '<thead><tr>' + fusionHeader.join('') + '</tr></thead>' );
    fusionTable.append( '<tfoot><tr>' + fusionHeader.join('') + '</tr></tfoot>' );

    fusionInspectorState.cache[ "fusionKeys" ] = orderTableKeysBeginning( forcedHeaderKeyOrder, fusionKeys );

    // Add data table body (in order of forced fusion header)
    fusionTable.append( '<tbody>' );
    for( var fusionIndex = 0; fusionIndex < fusionInspectorState.cache.json.fusions.length; fusionIndex++ ){
       var fusionEntry = fusionInspectorState.cache.json.fusions[ fusionIndex ];
       fusionTable.append( toTableBodyElement( fusionEntry, forcedHeaderKeyOrder ) );
    }
    fusionTable.append( '</tbody>' );

}

var sh='<div class="constainer-fluid" id="sampleHeader" style="background-color: #E7E7EF"></div>';
var navb='<nav class="navbar navbar-default" style="background-color: #E7E7EF"></nav>'
var fnd='<div class="col-xs-3" id="FusionNameDetail"><p class="navbar-text"><b>Fusion Name:</b> Not Selected</p></div>';
var fjd='<div class="col-xs-3" id="FusionJunctionDetail"><p class="navbar-text"><b>Junction Read Count:</b> Not Selected</p></div>';
var fsd='<div class="col-xs-3" id="FusionSpanningDetail"><p class="navbar-text"><b>Spanning Read Count:</b> Not Selected</p></div>';
$("body").append(sh,navb,fnd,fjd,fsd);

var tabDescription='<ul id="tabDescription" class="nav nav-tabs"></ul>';
var tabBrowser_tab='<li role="presentation" id="tabBrowser_tab" class="active"><a href="#tabBrowser" data-toggle="tab">Browse All Fusions</a></li>';
$("body").append(tabDescription,tabBrowser_tab);

var tab_content='<div class="tab-content" id="tabContent"></div>';
var tabpanel='<div role="tabpanel" id="tabBrowser" class="tab-pane fade in active" data-toggle="tab"></div>';
var table_responsive='<div class="table-responsive"></div>';
var fusionTable='<table id="fusionTable" class="table table-striped table-bordered table-hover active" cell spacing="0" width="100%"></table>';
$("body").append(tab_content,tabpanel,table_responsive,fusionTable);


$.getJSON("finspector.fusion_inspector_web.json", function(data){
     console.log("JSON DATA");
     console.log(data);
     $(document).ready(function( ) {
     // Load data
     fusionInspectorState.cache[ "json" ] = data;
     // Load the data table
     loadFusionDataTable();
     fusionInspectorState.cache.fusionTable = $('#fusionTable').DataTable({
             'order': [[1,'desc']],
             'scrollX': true
     });
     $('#fusionTable tbody').on('click', 'tr', function() {
            curFusionRow = fusionInspectorState.cache.fusionTable.row( this ).data();
         // IGV browser has to be visible when the files are loaded.
         // If it is hidden the files load as 200 (full file) as opposed
         // to 206, whichis needed for indexed reading as igv web needs it.
        loadIGVBrowser(
              getFusionAnnotationFromRow( 'Fusion', curFusionRow ),
              getFusionAnnotationFromRow( 'Junction Reads', curFusionRow ),
              getFusionAnnotationFromRow( 'Spanning Fragments', curFusionRow ),
              getFusionAnnotationFromRow( 'Right Pos', curFusionRow ),
              getFusionAnnotationFromRow( 'Left Pos', curFusionRow )
         );//loadIGVBrowser
      });//#fusionTable
         // This hooks into the event fired off by tabs being selected.
         // It forces a redraw of the tab. Because the data table is originally
         // draw in a hidden (height = 0) div, the table is misdrawn. You have to
         // Trigger a redraw when the tab is visible so the height of the data table
         // can be correctly calculated.
      $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
      $('#fusionTable').DataTable().columns.adjust().draw();
     })
   }); //Document.ready
}) //getJSON
