ObjC.import('Quartz');
function run(argv){
 var doc=$.PDFDocument.alloc.initWithURL($.NSURL.fileURLWithPath(argv[0]));
 var a=parseInt(argv[1]), b=parseInt(argv[2]), out=[];
 for(var i=a-1;i<b && i<doc.pageCount;i++){ out.push('=== Seite '+(i+1)+'\n'+ObjC.unwrap(doc.pageAtIndex(i).string)); }
 return out.join('\n');
}
