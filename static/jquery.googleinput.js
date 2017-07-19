//Author: Saurabh Pathak
;(function($){

  // Load the Google Transliteration API
  google.load("elements", "1", {
        packages: "transliteration"
      });

  $(window).on( "load", function() {

        var options = {
        sourceLanguage: 'en',
        destinationLanguage: 'hi',
        shortcutKey: 'ctrl+m',
        transliterationEnabled: true
        };

    // Create an instance on TransliterationControl with the required options.
    var control = new google.elements.transliteration.TransliterationControl(options);

    // Enable transliteration in the textfields with the given ids.
    var ids = ["text"];
    control.makeTransliteratable(ids);
  });

})(jQuery);
