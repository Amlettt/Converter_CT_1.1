// переписать все ошибки в один блок. Менять только текст. а не как сейчас на каждую ошибку свой блок
$(document).ready(function(){
    $("#convert").on("click", function(){
        //действия
        converting();
    });

    //фиксируем размер окна. При изменении размера меняем его назад
    // $(window).on('resize', function(){
    //     var win = $(this); //this = window
    //     if (win.height() > 520 || win.width() > 400) {
    //         win.width(400);
    //         win.height(520);
    //     }
    // });
    window.onresize = function (){
        if (window.outerWidth > 400 || window.outerHeight > 520){
            window.resizeTo(400, 520);
        }
    };

    // Показываем инструкцию
    $(document).on('click', '#instruction', function(){
        $('.window-block').addClass('visible');
        $('main').addClass("disable-hover");
    });

    $(document).on('click', '.close', function(){
        $('.window-block').removeClass('visible');
        $('main').removeClass("disable-hover");
    });

    // визуализация количества выбранных файлов
    $('.input__file').change(function () {
        let labelVal = $('.input__file-button-text').text();
        $('.form__convert-no').removeClass('visible');
        $('.form__convert-yes').removeClass('visible');
        $('.form__file-no').removeClass('visible');
        let countFiles = '';
        if (this.files && this.files.length >= 1)
            countFiles = this.files.length;

        if (countFiles)
          $('.input__file-button-text').text('Выбрано файлов: ' + countFiles);
        else
          $('.input__file-button-text').text(labelVal);
    });
 });

// конвертируем выбранный файл
async function converting() {
    let address, convert_yes;

    if (!$(".input__file").val() == "") {
        address = $('.input__file').val().split("\\"); // делим по двум чертам
        convert_yes = await eel.read_csv(address[2])(); // адрес 2 потому что путь разделенн на 3 части. нам нужна 3я
        $(".input__file").val(""); // сбросить выбранный файл
        $('.input__file-button-text').text('Выберите файл');

        if ($('.form__file-no').hasClass("visible")) {
            $('.form__file-no').removeClass('visible'); // удаляем класс индикация когда файл не выбран с дисплей block
        }
        if (convert_yes === 1) {
            $('.form__convert-yes').addClass('visible')  // добавляем класс индикация удачного чтения файла с дисплей block
            if ($('.form__convert-no').hasClass("visible")) {
                $('.form__convert-no').removeClass('visible'); // удаляем класс индикация не удачного чтения файла с дисплей none
            }
        }
    }
    else {
        if (!$('.form__file-no').hasClass("visible")) {
            $('.form__file-no').addClass('visible'); // добавляем класс индикация когда файл не выбран с дисплей block
        }
        if ($('.form__convert-no').hasClass("visible")) {
            $('.form__convert-no').removeClass('visible'); // удаляем класс индикация не удачного чтения файла с дисплей none
        }
        if ($('.form__convert-yes').hasClass("visible")) {
            $('.form__convert-yes').removeClass('visible'); // удаляем класс индикация удачного чтения файла с дисплей none
        }
    }
}






