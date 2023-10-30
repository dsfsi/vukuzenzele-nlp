import laser_config, file_handler, sentence_tokenisation, sentence_embedding, sentence_alignment
from itertools import combinations

languages = ['afr', 'eng', 'nbl', 'nso', 'sot', 'ssw', 'tsn', 'tso', 'ven', 'xho', 'zul']

lang_mappings = {
                    'afr' : '',
                    'eng' : '',
                    'nbl' : '',
                    'sot' : 'sot_Latn',
                    'nso' : 'nso_Latn',
                    'ssw' : 'ssw_Latn',
                    'tsn' : 'tsn_Latn',
                    'tso' : 'tso_Latn',
                    'ven' : '',
                    'xho' : 'xho_Latn',
                    'zul' : 'zul_Latn',
                } 


if __name__ == "__main__":
   
    # create directories dictionary
    filepaths_dictionary = file_handler.build_filepaths_dictonary()
    last_date = file_handler.extract_latest_edition()
    edition_keys = file_handler.fetch_data_edition_filepaths(last_date)
    language_pairs = list(combinations(languages, 2))


    if len(edition_keys) > 0:
        print('performing sentece aligment on new edtions...')
         # setup laser
        laser_config.set_environ_var()
        laser_config.setup_laser()
        laser_config.download_laser_models(lang_mappings)
        laser_config.download_tokeniser()

        # perform tokenisation
        print("Tokenising process started...")
        for edition in edition_keys:
            for lang in languages:
                if edition not in filepaths_dictionary[lang]:
                    continue
                for txt in filepaths_dictionary[lang][edition]:
                    # print(f"Edition: {edition} \t Lang: {lang} \t Text: {txt}")
                    text = file_handler.read_file_as_string(edition, txt)
                    tokens = sentence_tokenisation.tokenise(text)
                    file_handler.write_tokens_to_txt(edition, txt, tokens)
        print("Tokenising process complete.")


        # perform LASER encoding
        print("LASER encoding process started...")
        for edition in edition_keys:
            for lang in lang_mappings.keys():
                print("Encoding {} editions for {}".format(lang, edition))
                if edition not in filepaths_dictionary[lang]:
                    continue
                for txt in filepaths_dictionary[lang][edition]:
                    sentence_embedding.encode_sentences(edition, txt, lang_mappings[lang])
        print("LASER encoding process completed")


        # perform SA on LASER encoded sentences
        print("LASER aligning process started, output will be written to .csv in the data/opt_aligned_out folder.")
        for (first_lang, sec_lang) in language_pairs:
                for edition in edition_keys:
                    if edition == '2018-02-ed1': continue
                    sentence_alignment.sentence_alignment(first_lang, sec_lang, edition)
        print("LASER aligning completed")



        # # perform basic sentece alignment on tokenised sentences
        # print("Simple aligning process started, output will be written to .csv in the data/simple_align_output folder.")
        # for (first_lang, sec_lang) in language_pairs:
        #     for edition in edition_keys:
        #         sentence_alignment.simple_langs_alignment(first_lang, sec_lang, edition)
        # print("Simple aligning completed")
        
        # write last edition reviewed to file so as not to review in future
        file_handler.write_latest_edition(edition_keys[len(edition_keys)-1])
        # file_handler.count_aligned_pairs()
    else: print('No new editions present to perform sentence alignment')

