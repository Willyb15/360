var duration;
//Variable to prevent multiple Starts firing 
var movieState = false;
//Grab the Video Name
var title = $(".card__header__info__title")[0].innerHTML;
_satellite.setVar("title",title);

jwplayer().on('play',function(){
      //Grab the length of the Video

  if(_satellite.getVar('movieState') !== true){
     duration = Math.floor(jwplayer().getDuration());
    _satellite.setVar("duration", duration);
    _satellite.track("JW_3d_Start");
    _satellite.setVar("movieState", true);
  }
});
//Any Video Complete 
//Dont think this is effected by ads
jwplayer().on('complete',function(){
	_satellite.track("JW_3d_Finish");
	_satellite.setVar("movieState", false);
});



function checkPalindrome(str) {
	str = str.toLowerCase().replace(/[^a-z]+/g,"");
	// if(str === str.split("").reverse().join("")){
 //  		return true
 // 	}else
 //  	return false
 // 	}
}


// increases by 4 each setTimeout(function()
// n=1, a=1
// n=2, a=5
// n=3, a=5+8
// n=4, a=12+12

function calculateArea(n){
	var multiplier = 4*n;
	

}



























