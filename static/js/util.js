function $(p){
	if(/^<([a-zA-Z]+)>$/.test(p)){
		return document.createElement(RegExp.$1);
	}else{
		return document.querySelectorAll(p);
	}
}

function trim(str){ 
	return str.replace(/(^\s*)|(\s*$)/g, "");
}


function getTop(e){
   var offset=e.offsetTop;
   if(e.offsetParent!=null) {
	   offset+=getTop(e.offsetParent);
   }
   return offset;
}


function getLeft(e){
   var offset=e.offsetLeft;
   if(e.offsetParent!=null){
	   offset+=getLeft(e.offsetParent);
   }
   return offset;
}

function remove(q){
	var eles = $(q);
	for(var i=0;i<eles.length;i++){
		var ele = eles[i];
		ele.parentNode.removeChild(ele);
	}
}