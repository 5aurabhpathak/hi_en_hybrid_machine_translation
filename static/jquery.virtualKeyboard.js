//Author: Saurabh Pathak
;(function($){

    var defaults = {
        styleClassParentInput: 'vkb-css-parent-input',
        styleClassKeyboardIcon: 'vkb-css-keyboard-icon',
        srcKeyboardIcon: "static/keyboard.png"
    };

    var virtualKeyboard = {
        template: '<div id="vkb-js-keyboard" class="vkb-css-hide"><div class="vkb-css-background vkb-js-close"></div><div class="vkb-css-keyboard-box"><div class="vkb-css-input-box"><input type="text" id="vkb-js-input" class="vkb-css-input"/></div><div id="vkb-buttons" class="vkb-css-button-box"><div class="vkb-css-button-line"><button type="button">ँ</button> <button type="button">ं</button> <button type="button">ः</button><button type="button">ऽ</button> <button type="button">्</button> <button type="button">ॐ</button><button type="button">्र</button> <button type="button">ॠ</button></div><div class="vkb-css-button-line"> <button type="button">ा</button> <button type="button">ि</button> <button type="button">ी</button> <button type="button">ु</button> <button type="button">ू</button> <button type="button">े</button> <button type="button">ै</button> <button type="button">ो</button> <button type="button">ौ</button> <button type="button">ृ</button></div><div class="vkb-css-button-line"> <button type="button">१</button> <button type="button">२</button> <button type="button">३</button> <button type="button">४</button> <button type="button">५</button> <button type="button">६</button> <button type="button">७</button> <button type="button">८</button> <button type="button">९</button> <button type="button">०</button></div><div class="vkb-css-button-line"> <button type="button">अ</button> <button type="button">आ</button> <button type="button">इ</button> <button type="button">ई</button> <button type="button">उ</button> <button type="button">ऊ</button> <button type="button">ए</button> <button type="button">ऐ</button> <button type="button">ओ</button> <button type="button">औ</button><button type="button">अं</button> <button type="button">अ:</button></div><div class="vkb-css-button-line"> <button type="button">क</button> <button type="button">ख</button> <button type="button">ग</button> <button type="button">घ</button> <button type="button">ङ</button> <button type="button">च</button> <button type="button">छ</button> <button type="button">ज</button> <button type="button">झ</button> <button type="button">ञ</button> </div><div class="vkb-css-button-line"> <button type="button">ट</button> <button type="button">ठ</button> <button type="button">ड</button> <button type="button">ढ</button><button type="button">ण</button> <button type="button">प</button> <button type="button">फ</button><button type="button">ब</button> <button type="button">भ</button> <button type="button">म</button>  </div><div class="vkb-css-button-line"> <button type="button">त</button> <button type="button">थ</button> <button type="button">द</button> <button type="button">ध</button><button type="button">न</button> <button type="button">य</button> <button type="button">र</button><button type="button">ल</button> <button type="button">व</button> <button type="button">स</button>  </div><div class="vkb-css-button-line"> <button type="button">ष</button> <button type="button">श</button> <button type="button">ह</button> <button type="button">क्ष</button><button type="button">त्र</button> <button type="button">ज्ञ</button></div><div class="vkb-css-button-line"> <button type="button">क़</button> <button type="button">ख़</button> <button type="button">ग़</button> <button type="button">ज़</button> <button type="button">फ़</button> <button type="button">.र</button> <button type="button">ऩ</button> <button type="button">य़</button></div></div><p style="font-size:12px;">Use hardware keyboard for punctuation.</p><div class="vkb-css-footer-box"><button type="button" id="vkb_close">Cancel</button> <button type="button" id="vkb_success">OK</button></div></div></div>',
        shifted: false,
        clickSumbolButton: function (e) {
            return function (e) {
                switch($(e.currentTarget).attr('id')) {
                    case "vkb_close":
                        this.keyboard.hide();
                        this.input.val('');
                        break
                    case "vkb_success":
                        this.source.val(this.input.val());
                        this.keyboard.hide();
                        break
                    default:
                        this.pasteSymbolInPosition($(e.currentTarget).html());
                }
            }
        },
        show: function ($source) {
            this.source = $source;
            this.input.val(this.source.val());
            this.keyboard.show();
        },
        pasteSymbolInPosition: function (symbol) {
                var selectionStart = (!symbol.length && this.input[0].selectionStart === this.input[0].selectionEnd && this.input[0].selectionStart !== 0) ? this.input[0].selectionStart - 1 : this.input[0].selectionStart;
                var parth1 = this.input.val().slice(0, selectionStart);
                var parth2 = this.input.val().slice(this.input[0].selectionEnd, this.input.val().length);
                this.input.val(parth1 + symbol + parth2);
                this.setCursorPosition(selectionStart + symbol.length);
                this.input.focus();
        },
        setCursorPosition: function (position) {
            if (this.input[0].setSelectionRange) {
                this.input[0].setSelectionRange(position, position);
            } else if (this.input[0].createTextRange) {
                var range = this.input[0].createTextRange();
                range.collapse(true);
                range.moveEnd('character', position);
                range.moveStart('character', position);
                range.select();
            }
        this.input.focus();
        }
    }

    function Vkb(element, options) {
        this.config = $.extend({}, defaults, options);
        this.element = element;
        this.init();
    }

    Vkb.prototype.init = function () {

        this.element.addClass(this.config.styleClassParentInput);

        $('body').append(virtualKeyboard.template);
        virtualKeyboard.keyboard = $('#vkb-js-keyboard');
        virtualKeyboard.input = $('#vkb-js-input');
        $('#vkb-js-keyboard').on('click',  'button', $.proxy(virtualKeyboard.clickSumbolButton(this), virtualKeyboard));

        $('<img/>',{
            alt: 'Keyboard',
            src: this.config.srcKeyboardIcon,
            class: this.config.styleClassKeyboardIcon + ' vkb-js-key'
        })
            .insertAfter(this.element)
            .on('click', function(e) {
                virtualKeyboard.show($(e.currentTarget).prev('textarea'));
                $('#vkb-js-input').val($(e.currentTarget).prev('textarea').val()).focus();
            });
    }

    $.fn.vkb = function (options) {
        new Vkb(this, options);
        return this;
    }

})(jQuery);
