document.getElementById('convert-form').addEventListener('submit', function(event) {
    var url = document.getElementById('url').value;
    if (!url) {
        event.preventDefault();
        document.getElementById('message').textContent = "Please enter a valid YouTube URL.";
    } else {
        document.getElementById('message').textContent = "";
    }
});

document.getElementById('url').addEventListener('input', function() {
    var url = this.value;
    var videoId = getYouTubeVideoId(url);
    if (videoId) {
        var thumbnailUrl = `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`;
        var thumbnail = document.getElementById('thumbnail');
        thumbnail.src = thumbnailUrl;
        thumbnail.classList.remove('hidden');
    } else {
        document.getElementById('thumbnail').classList.add('hidden');
    }
});

function getYouTubeVideoId(url) {
    var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
    var match = url.match(regExp);
    return (match && match[2].length == 11) ? match[2] : null;
}
