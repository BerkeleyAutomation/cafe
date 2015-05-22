$(window).ready(function() {
	$('.listen').click(function() {
		var blob = this.getAttribute('sound-blob');
		if (blob != null) {
			audio_source.src = blob;
		} else {
			audio_source.src = window.url_root + '/media/audio/' + this.getAttribute('sound') + '.wav';
		}
		audio_player.load();
		audio_player.play();
	});
});

	  function __log(e, data) {
    console.log(e, data);
    // log.innerHTML += "\n" + e + " " + (data || '');
  }

    window.onload = function init() {
    try {
      // webkit shim
      window.AudioContext = window.AudioContext || window.webkitAudioContext;
      navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia;
      window.URL = window.URL || window.webkitURL;

      audio_context = new AudioContext;
      __log('Audio context set up.');
      __log('navigator.getUserMedia ' + (navigator.getUserMedia ? 'available.' : 'not present!'));
    } catch (e) {
      alert('No web audio support in this browser!');
    }

    navigator.getUserMedia({audio: true}, startUserMedia, function(e) {
      __log('No live audio input: ' + e);
    });
  };

    function startUserMedia(stream) {
    var input = audio_context.createMediaStreamSource(stream);
    __log('Media stream created.');

    recorder = new Recorder(input);
    __log('Recorder initialised.');
  }

  function startRecording(button) {
    recorder && recorder.record();
    // $(".startRecording").button('disable'); //disabled = true;
    $(".stopRecording").css('visibility', 'visible');
    $(".startRecording").css('visibility', 'hidden');
    $(".listenComment").css('visibility', 'hidden');
    // button.nextElementSibling.disabled = false;
    __log('Recording...');
  }

  function stopRecording(button) {
    recorder && recorder.stop();
    // $(".stopRecording").button('disable');
    // $(".startRecording").button('enable');
    $(".startRecording").css('visibility', 'visible');
    $(".stopRecording").css('visibility', 'hidden');

    $(".listenComment").css('visibility', 'visible');
    __log('Stopped recording.');

    // create WAV download link using audio data blob
    createDownloadLink();

    recorder.clear();
  }

  function createDownloadLink() {
    recorder && recorder.exportWAV(function(blob) {
      var url = URL.createObjectURL(blob);
      $(".listenComment").attr("sound-blob", url);
      var li = document.createElement('li');
      var au = document.createElement('audio');
      var hf = document.createElement('a');

      au.controls = true;
      au.src = url;
      hf.href = url;
      hf.download = new Date().toISOString() + '.wav';
      hf.style.setProperty("color", "#49311c", "important");
      hf.innerHTML = hf.download;
      li.appendChild(au);
      li.appendChild(hf);
      //recordingslist.appendChild(li);

      var data = new FormData();
      data.append('file', blob);

      /* $.ajax({
        url :  "/os/saveaudio/",
        type: 'POST',
        data: data,
        contentType: false,
        processData: false,
        success: function(data) {
          alert("worked!");
        },
        error: function() {
          alert("didn't work!");
        }
      }); */
    });
  }