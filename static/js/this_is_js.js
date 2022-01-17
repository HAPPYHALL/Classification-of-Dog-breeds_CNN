function to_index() {
    window.location.href = "/"
}


// function to_main() {
//     window.location.href = "/main"
//
// }

function to_upload() {
    window.location.href = "/upload"

}


//업로드 기능 구현


// 사진 보이기
    var fileInput = document.getElementById("inputFile");
    //값이 변경될때 호출 되는 이벤트 리스너
    console.log(fileInput)
    fileInput.addEventListener('change', function (e)

    {
        var file = e.target.files[0]; //선택된 파일
        var reader = new FileReader();
        reader.readAsDataURL(file); //파일을 읽는 메서드

        reader.onload = function () {
            var photoFrame = document.createElement("div");
            photoFrame.style = `background : url(${reader.result}); object-fit: fill; background-size : cover`;
            photoFrame.className = "photoFrame";
            document.getElementById("pictures").appendChild(photoFrame);



        }
    })

 function posting() {
    let file = $('#inputFile')[0].files[0]
    let form_data = new FormData()

    form_data.append("file_give", file)
    console.log(form_data)
     console.log(file)
    $.ajax({
        type: "POST",
        url: "/fileupload",
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            alert(response["result"])
            // 아래처럼 하지 않아도, 백엔드(app.py)에서 바로 판별 함수를 실행한 뒤에
            // render_template 을 해서 바로 결과 페이지로 넘어가도 됨
            window.location.href='/main'
        }
    });
  }

  function preview() {
    let frame = $('#frame');
    frame.src=URL.createObjectURL(event.target.files[0]);
  }

