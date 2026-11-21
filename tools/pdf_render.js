ObjC.import('Quartz'); ObjC.import('AppKit');
function run(argv){
 var doc=$.PDFDocument.alloc.initWithURL($.NSURL.fileURLWithPath(argv[0]));
 var n=doc.pageCount, sc=parseFloat(argv[2]||'2');
 for(var i=0;i<n;i++){
  var p=doc.pageAtIndex(i); var r=p.boundsForBox(0);
  var img=p.thumbnailOfSizeForBox($.NSMakeSize(r.size.width*sc,r.size.height*sc),0);
  var rep=$.NSBitmapImageRep.imageRepWithData(img.TIFFRepresentation);
  rep.representationUsingTypeProperties($.NSBitmapImageFileTypePNG,$()).writeToFileAtomically(argv[1]+'/p'+('0'+(i+1)).slice(-2)+'.png',true);
 }
 return n+' pages, '+r.size.width+'x'+r.size.height;
}
