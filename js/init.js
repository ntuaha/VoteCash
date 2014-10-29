

var votedata=null;

function readData(){
  votedata = d3.csv.parse("./data/votedata.csv");
}



$(function(){
  readData();


});
