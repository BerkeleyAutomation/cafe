//loading data
var xmlhttp;
var data;
var number_time_point=4;
// xValue[i][j] user j's x at i timepoint
var xValue=new Array(number_time_point);
var yValue=new Array(number_time_point);
var number_user=new Array();

function load(url,cfunc)
{
  
  if (window.XMLHttpRequest){// code for IE7+, Firefox, Chrome, Opera, Safari
  xmlhttp=new XMLHttpRequest();
  }
  else{// code for IE6, IE5
  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
  xmlhttp.onreadystatechange=cfunc
  xmlhttp.open("GET",url,true);
  xmlhttp.send();
}

function getPosition()
{
   load("data.xml",function(){
      if (xmlhttp.readyState==4 && xmlhttp.status==200){
	      data=xmlhttp.responseXML;
	      for (var i=0; i<number_time_point; i++){
               var currentX=new Array();
               var currentY=new Array();
               var user_number=data.getElementsByTagName('x'+i.toString());
               number_user[i]=user_number.length;
               for (var j=0; j<number_user[i]; j++){                          
		         currentX[j]=data.getElementsByTagName('x'+i.toString())[j].childNodes[0].nodeValue;
		         currentY[j]=data.getElementsByTagName('y'+i.toString())[j].childNodes[0].nodeValue;
	           }
               xValue[i]=currentX;
               yValue[i]=currentY;	  
          }
          init();           
      }
   }); 
}


//Animation
var canvas;
var ctx;
var background;

var width;
var height;

var mug=new Array(); //store mug image 1-dim
var mug_x=new Array(); // record user i's position at given time point from data 2-dim
var mug_y=new Array(); // 2-dim
var mug_x_current=new Array(); //used in update 1-dim
var mug_y_current=new Array();
var speed_ratio=new Array(); //record user i's speed on x axis from point j to point j+1, 2-dim
var x_vel_direction=new Array(); //velocity=direction*speed_ratio 2-dim
var y_vel_direction=new Array();
var x_vel_current=new Array();
var y_vel_current=new Array();
var time_thresholds=new Array; // used to check which velocity to use
var time_steps=0; //accumulate thorugh update
function init() {
	
	canvas = document.getElementById("MugAnimation");
	width = canvas.width;
	height = canvas.height;
	ctx = canvas.getContext("2d");

	// init mug
    for (var i=0; i<number_user[number_time_point-1]; i++)
    {
       mug[i] = new Image();
	   mug[i].src = 'cafe'+(Math.round(Math.random()*5)).toString()+'.png';
    }
    // assign position
    for (var i=0; i<number_time_point; i++){
       var i_x_Position=new Array();
       var i_y_Position=new Array();
       for (var j=0; j<number_user[i]; j++)       
       {
	       i_x_Position[j] = xValue[i][j]*width;
           i_y_Position[j] = yValue[i][j]*height;
       }
       mug_x[i]=i_x_Position;
       mug_y[i]=i_y_Position;
    }
    
    // calculate speed and velocity for each transition
    
    for (var i=0; i<number_time_point-1; i++)
    {
       ref_dis=Math.sqrt(Math.pow(mug_x[i+1][0]-mug_x[i][0],2)+Math.pow(mug_y[i+1][0]-mug_y[i][0],2));
       if (i==0){
       time_thresholds[i]=ref_dis;}
       else{
       time_thresholds[i]=time_thresholds[i-1]+ref_dis;     // calulate threshold
       }
       var currentRatio=new Array();
       currentRatio[0]=1;
       for (var j=1; j<number_user[i]; j++)
       {
           currentRatio[j]=Math.sqrt(Math.pow(mug_x[i+1][j]-mug_x[i][j],2)+Math.pow(mug_y[i+1][j]-mug_y[i][j],2))/ref_dis;
       }
       speed_ratio[i]=currentRatio;       
    }

    for (var i=0; i<number_time_point-1; i++)
    {
        var x_dir=new Array();
        var y_dir=new Array();
        for (var j=0; j<number_user[i]; j++)
        {
            var dist=Math.sqrt(Math.pow(mug_x[i+1][j]-mug_x[i][j],2)+Math.pow(mug_y[i+1][j]-mug_y[i][j],2));
            x_dir[j]=(mug_x[i+1][j]-mug_x[i][j])/dist;
            y_dir[j]=(mug_y[i+1][j]-mug_y[i][j])/dist;
        }
        x_vel_direction[i]=x_dir;
        y_vel_direction[i]=y_dir;
    }
    /*console.log(number_user);
    console.log(xValue);
    console.log(yValue);
    console.log(mug_x);
    console.log(mug_y);
    console.log(speed_ratio);
    console.log(x_vel_direction);
    console.log(y_vel_direction);*/
    //assign initial position
    mug_x_current=mug_x[0];
    mug_y_current=mug_y[0];
    draw();
    
}

function update(){
    if (time_steps<time_thresholds[0])
    {
        x_vel_current=x_vel_direction[0];
        y_vel_current=y_vel_direction[0];
	    for (var i=0; i<number_user[0]; i++)
        {    
           mug_x_current[i]=mug_x_current[i]+x_vel_current[i]*speed_ratio[0][i];
           mug_y_current[i]=mug_y_current[i]+y_vel_current[i]*speed_ratio[0][i];           
        }
        
        if (time_steps-(time_thresholds[0]-1)>=0)
        {
			for (var j=number_user[0]; j<number_user[1]; j++)
			{
				mug_x_current[j]=mug_x[1][j];
				mug_y_current[j]=mug_y[1][j];
			}
		}
        time_steps+=1; 
        
    }
    else if(time_steps>=time_thresholds[0] && time_steps<time_thresholds[1])
    {
               
        x_vel_current=x_vel_direction[1];
        y_vel_current=y_vel_direction[1];
        for (var i=0; i<number_user[1]; i++)
        {    
           mug_x_current[i]=mug_x_current[i]+x_vel_current[i]*speed_ratio[1][i];
           mug_y_current[i]=mug_y_current[i]+y_vel_current[i]*speed_ratio[1][i];           
        }
        if (time_steps-(time_thresholds[1]-1)>=0)
        {
			for (var j=number_user[1]; j<number_user[2]; j++)
			{
				mug_x_current[j]=mug_x[2][j];
				mug_y_current[j]=mug_y[2][j];
			}
		}
        time_steps+=1; 
    }
    else if (time_steps>=time_thresholds[1] && time_steps<time_thresholds[2])
    {
		x_vel_current=x_vel_direction[2];
        y_vel_current=y_vel_direction[2];
        for (var i=0; i<number_user[2]; i++)
        {    
           mug_x_current[i]=mug_x_current[i]+x_vel_current[i]*speed_ratio[2][i];
           mug_y_current[i]=mug_y_current[i]+y_vel_current[i]*speed_ratio[2][i];           
        }
        time_steps+=1; 
	}
}
 
function draw() {
    ctx.clearRect(0,0,canvas.width,canvas.height);
    if (time_steps<time_thresholds[0]){
		for (var i=0; i<number_user[0]; i++)
        {
            ctx.drawImage(mug[i], mug_x_current[i], mug_y_current[i],mug[i].width/4,mug[i].height/4);
        }
	}
    else if(time_steps>=time_thresholds[0] && time_steps<time_thresholds[1])
    {
		for (var i=0; i<number_user[1]; i++)
        {   
            ctx.drawImage(mug[i], mug_x_current[i], mug_y_current[i],mug[i].width/4,mug[i].height/4);
        }
	}
	else
	{
		for (var i=0; i<number_user[2]; i++)
        {   
            ctx.drawImage(mug[i], mug_x_current[i], mug_y_current[i],mug[i].width/4,mug[i].height/4);
        }
	}
	
		
}
 
function main_loop() {
	draw();
	update();
}

function clickreset(){
	time_steps=0;
	init();
	setInterval(main_loop, 15);
}
	
getPosition();

