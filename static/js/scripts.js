// document.getElementById('convert-form').addEventListener('submit', function(event) {
//     var url = document.getElementById('url').value;
//     if (!url) {
//         event.preventDefault();
//         document.getElementById('message').textContent = "Please enter a valid YouTube URL.";
//     } else {
//         document.getElementById('message').textContent = "";
//     }
// });

// document.getElementById('url').addEventListener('input', function() {
//     var url = this.value;
//     var videoId = getYouTubeVideoId(url);
//     if (videoId) {
//         var thumbnailUrl = `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`;
//         var thumbnail = document.getElementById('thumbnail');
//         thumbnail.src = thumbnailUrl;
//         thumbnail.classList.remove('hidden');
//     } else {
//         document.getElementById('thumbnail').classList.add('hidden');
//     }
// });

// function getYouTubeVideoId(url) {
//     var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
//     var match = url.match(regExp);
//     return (match && match[2].length == 11) ? match[2] : null;
// }

document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('convert-form');
    var urlInput = document.getElementById('url');
    var message = document.getElementById('message');
    var thumbnail = document.getElementById('thumbnail');
    var thumbnailContainer = document.getElementById('thumbnail-container');
    var downloadBtn = document.getElementById('download-btn');
    var btnSpinner = document.getElementById('btn-spinner');
    var btnText = document.getElementById('btn-text');
    var qualitySelect = document.getElementById('quality');

    function showToast(text, type) {
        var toastEl = document.getElementById('app-toast');
        var toastBody = document.getElementById('app-toast-body');
        toastBody.textContent = text;
        toastEl.classList.remove('bg-success', 'bg-danger');
        toastEl.classList.add(type === 'success' ? 'bg-success' : 'bg-danger');
        var bsToast = new bootstrap.Toast(toastEl);
        bsToast.show();
    }

    function showAlert(text, type) {
        message.className = 'alert alert-' + (type || 'danger');
        message.textContent = text;
        message.classList.remove('d-none');
        // also show a toast for better visibility
        showToast(text, type);
    }

    function clearAlert() {
        message.className = 'alert d-none';
        message.textContent = '';
    }

    form.addEventListener('submit', function (event) {
        var url = urlInput.value.trim();
        if (!url) {
            event.preventDefault();
            showAlert('Please enter a valid URL.', 'danger');
            return;
        }

        // Micro animation on button for feedback
        downloadBtn.classList.add('btn-pop');
        setTimeout(function () { downloadBtn.classList.remove('btn-pop'); }, 300);

        // Show spinner and disable button while request proceeds
        btnSpinner.classList.remove('d-none');
        downloadBtn.setAttribute('disabled', 'disabled');
        clearAlert();
    });

    urlInput.addEventListener('input', function () {
        var url = this.value.trim();
        var videoId = getYouTubeVideoId(url);
        if (videoId) {
            var thumbnailUrl = 'https://img.youtube.com/vi/' + videoId + '/hqdefault.jpg';
            thumbnail.src = thumbnailUrl;
            // show container then animate thumbnail (animate.css + CSS fallback)
            thumbnailContainer.classList.remove('d-none');
            thumbnailContainer.classList.remove('show');
            thumbnail.classList.remove('animate__animated', 'animate__fadeInUp');
            // force reflow to retrigger animation
            void thumbnail.offsetWidth;
            thumbnail.classList.add('animate__animated', 'animate__fadeInUp');
            // CSS fallback
            thumbnailContainer.classList.add('show');
            qualitySelect.parentElement.classList.remove('d-none');
            clearAlert();
        } else if (url.includes('instagram.com')) {
            thumbnailContainer.classList.add('d-none');
            thumbnailContainer.classList.remove('show');
            qualitySelect.parentElement.classList.add('d-none');
            clearAlert();
        } else {
            thumbnailContainer.classList.add('d-none');
            thumbnailContainer.classList.remove('show');
            qualitySelect.parentElement.classList.remove('d-none');
            clearAlert();
        }
    });

    function getYouTubeVideoId(url) {
        var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
        var match = url.match(regExp);
        return (match && match[2].length == 11) ? match[2] : null;
    }

});

