$(document).ready(function() {
    updateWindowList();

    $('#update-window-list').click(function() {
        updateWindowList();
    });

    $('#window-select').change(function() {
        const windowTitle = $(this).val();
        if (windowTitle) {
            setInterval(() => {
                getWindowImage(windowTitle);
            }, 1000);
        }
    });
});

function updateWindowList() {
    $.get('/get_windows', function(windows) {
        const windowSelect = $('#window-select');
        windowSelect.empty();
        windowSelect.append('<option value="">Select a window</option>');
        windows.forEach(function(window) {
            windowSelect.append('<option value="' + window + '">' + window + '</option>');
        });
    });
}

function getWindowImage(windowTitle) {
    $.ajax({
        url: '/get_window_image',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ window_title: windowTitle }),
        success: function(response) {
            const image = new Image();
            image.src = 'data:image/jpeg;base64,' + response.image;
            $('#window-image').attr('src', image.src);
        },
        error: function() {
            console.error('Failed to get window image');
        }
    });
}
