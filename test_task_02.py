from checkout import checkout, OUT_FOLDER, FOLDER_FOLDER, TEXT_FAIL, ARC_TYPE


class TestNegative:

    def test_step1(self, make_folder, clean_folder, make_files, make_bad_archive):
        assert checkout(f'cd {OUT_FOLDER}; 7z e bad.{ARC_TYPE} -o{FOLDER_FOLDER} -y', TEXT_FAIL), "test1 FAIL"
