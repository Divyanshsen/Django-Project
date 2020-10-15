window.onload = initAll;


function initAll(){

	getAllElements();

	setAllElements();

}

var todotype,chklst_img,txtnote_img,settxt,svbtn,title,ttl_txt_1;
var _todo_id_1,hidden_inp,textnote_box,ttl_type_,ttl_del_,ttl_sv_;

function getAllElements(){
	chklst_img = document.getElementById('chklst');
	txtnote_img = document.getElementById('txtnote');
	settxt = document.getElementById('urselectiontxt');
	svbtn =	document.getElementById('sbm_btn');
	title =	document.getElementById('title');
	//ttl_txt_1 = document.getElementById('ttl_txt_1');
	ttl_sv_=document.getElementById('ttl_sv_');
	textnote_box=document.getElementById('textnote_main_box');
	ttl_type_=document.getElementById('ttl_type_');
		ttl_del_=document.getElementById('ttl_del_');


	var i=1;

	while(true){

		hdnfield = document.getElementById("_todo_id_"+i);
		ttlsp	= document.getElementById("ttl_txt_"+i);
		txtnote_data = document.getElementById("txnote_data_"+i);
		ttl_edit = document.getElementById("ttl_edit_"+i);
		loader = document.getElementById("_loader_"+i);
		created = document.getElementById("_created_"+i);
		todotype = document.getElementById("_todotype_id_"+i);
		edit = document.getElementById("_edit_"+i);
		del = document.getElementById("_del_"+i++);

		if(!hdnfield){
			break;
		}
		else{
			todo_id=hdnfield.value;
			txtnote_data=txtnote_data.innerHTML;
			ttlsp.text=ttlsp.innerHTML;
			ttlsp.created=created.innerHTML;
			ttlsp.todotypeid=todotype.value;
			ttlsp.todoid=todo_id;
			ttlsp.onclick = ShowTodoBox;

			del.todotype=todotype.value;
			del.created=created.innerHTML;
			del.todoid=hdnfield.value;

			edit.todotype=todotype.value;
			edit.created=created.innerHTML;
			edit.todoid=hdnfield.value;
			
			del.onclick=deleteTodo;


			edit.onclick= function(){
							recs_id=this.id.substring(6);
							hfld=document.getElementById('ttl_edit_'+recs_id);
							ttl=document.getElementById('ttl_txt_'+recs_id);
							hfld.value=ttl.innerHTML;
							ttl.style.display="none";
							
							hfld.style.display="inline";
							hfld.todotype=this.todotype;
							hfld.todoid=this.todoid;
							hfld.created=this.created;
							hfld.focus();

							hfld.onblur=SaveNewTitle;
							
						  };

		}
	}
}

function ShowTodoBox(){
	main_table.style.display = 'none';
	_ttl_common.style.display = 'block';
	_ttl_txt.innerHTML = this.innerHTML;
	_ttl_created.innerHTML = this.created;
	ttl_del_.todoid=this.todoid;
	_ttl_todotypeid=this.todotypeid;
	_ttl_todoid=this.todoid;
	
	ttl_del_.onclick = deleteTodo;

	ttl_sv_.todoid=this.todoid;

	if(_ttl_todotypeid==1){
		// TextNote
		ttl_type_.src="/static/images/textnote.png";
		textnote_box.style.display="block";
		
		showTextNotes(this.todoid);
		ttl_sv_.onclick= savetextnotepoints;
	}
	else{
		//Checklist
		ttl_type_.src="/static/images/checklist.png";
		checklist_main_box.style.display="block";

		getchecklistpoints(this.todoid);
				
	}		

}

var reqpoint;
function getchecklistpoints(todoid){
	reqpoint= new XMLHttpRequest();
	url="/todoapp/getchecklistpoints/?todoid="+todoid;
	reqpoint.open('get',url,false);
	reqpoint.onreadystatechange=getAllPoint;
	reqpoint.send();

}

function getAllPoint(){
	if(reqpoint.readyState==4 && reqpoint.status==200){
		alert(reqpoint.responseText);

		resp=reqpoint.responseText;

		obj=JSON.parse(resp);
		alert(obj[1])
		//alert(obj.length);
		dv=document.getElementById('_chk_container_');

		/*
		for(i=1;i<obj.length;i++){
			//createInputCheckListField(dv)
			inp=document.createElement('input');
			inp.value=obj.todopoint+i;
			alert(obj.todopoint+i);

			inp.className='todopoint_inp';
			dv.appendChild(inp);
		
		}*/
		
	
	}
}
/*
createInputCheckListField(dv){
			inp=document.createElement('input');
			inp.value=obj.todopoint+i;
			inp.className='todopoint_inp';
			dv.appendChild(inp);
		}*/

var showtxtnote;
function showTextNotes(todoid){
	showtxtnote = new XMLHttpRequest();
	url='/todoapp/getalltxtnote/?todoid='+todoid;
	
	showtxtnote.open('get',url,false);
	showtxtnote.onreadystatechange=gettxtNote;
	showtxtnote.send();
}

function gettxtNote(){
	if(showtxtnote.readyState==4 && showtxtnote.status==200){
		var text=showtxtnote.responseText
		
		if(text!="None"){
			txnote_edit_box.value=text;
		}else{
			txnote_edit_box.value="Create Your TextNote Here ..!!"
		}
	}
}


var svreq;
function savetextnotepoints(){
	textnote=txnote_edit_box.value;
	svreq = new XMLHttpRequest();
	url="/todoapp/savetextNote/?todoid="+this.todoid+"&recs="+textnote;
	
	svreq.open('get',url,false);
	svreq.setRequestHeader('Content-Type','text/plain');
	svreq.onreadystatechange=savetxtNote;
	svreq.send();

}

function savetxtNote(){
	if(svreq.readyState==4 && svreq.status==200){
		alert(svreq.responseText)
	}
}


var delreq;
function deleteTodo(){
	id=this.todoid;
	
	delreq= new XMLHttpRequest();
	delreq.open("get","/todoapp/delrec/?todoid="+id,false);

	delreq.onreadystatechange= delRecord;

	delreq.send();


}

function delRecord(){
	if(delreq.readyState==4 && delreq.status==200){
		if(delreq.responseText);
			window.location="/todoapp/showtodo/"
	}
}

var svttl;
function SaveNewTitle(){
	new_title=this.value;
	todotype=this.todotype;
	todoid=this.todoid;
	created=this.created;
	
	svttl = new XMLHttpRequest;
	url="/todoapp/savenewttl/?id="+todoid+"&title="+new_title;
	svttl.open("get",url,false);
	svttl.onreadystatechange=SaveTitle;
	svttl.send();

}

function SaveTitle(){
	if (svttl.readyState==4 && svttl.status==200){
		if(svttl.responseText=="done"){
			window.location="/todoapp/showtodo";
		}
		
	}

}


function setAllElements(){

	chklst_img.onclick=function(){
							this.src="/static/images/checklist.png"
							this.style.boxShadow ="rgb(25, 103, 126) 7px 20px 20px";
							
							settxt.innerHTML="CheckList";
							settxt.todotype=1;

							txtnote_img.src="/static/images/chklist__.png"
							txtnote_img.style.boxShadow ="";
							
							
						};

	txtnote_img.onclick=function(){
							this.src="/static/images/textnote_.png"
							this.style.boxShadow ="rgb(25, 103, 126) 7px 20px 20px";
							settxt.innerHTML="TextNote";
							settxt.todotype=2;

							chklst_img.src="/static/images/checklist.png"
							chklst_img.style.boxShadow ="";
						
						};

	svbtn.onclick= SaveMyTodo;

}

var req;
function SaveMyTodo(){
	ttl=title.value;
	req = new XMLHttpRequest();
	req.open('get',"/todoapp/savetodo/?title="+ttl+"&todotypeid="+settxt.todotype,false)
	req.onreadystatechange= SaveNewTodo;
	req.send();

}

function SaveNewTodo(){
	if(req.readyState==4 && req.status==200){
		if(req.responseText=="done");
			window.location="/todoapp/showtodo/";
	}

}

