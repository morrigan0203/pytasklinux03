from checkout import checkout, getout, TST_FOLDER, OUT_FOLDER, FOLDER_FOLDER, TEXT_OK, ARC_TYPE


class TestPositive:

    def test_step1(self, make_folder, clean_folder, make_files):
        # test1
        res1 = checkout(f'cd {TST_FOLDER}; 7z a -t{ARC_TYPE} {OUT_FOLDER}/arx2', TEXT_OK)
        res2 = checkout(f'ls {OUT_FOLDER};', f'arx2.{ARC_TYPE}')
        assert res1 and res2, "test1 FAIL"

    def test_step2(self, clean_folder, make_files):
        # test2
        res = []
        res.append(checkout(f'cd {TST_FOLDER}; 7z a -t{ARC_TYPE} {OUT_FOLDER}/arx2', TEXT_OK))
        res.append(checkout(f'cd {OUT_FOLDER}; 7z e arx2.{ARC_TYPE} -o{FOLDER_FOLDER} -y', TEXT_OK))
        for i in make_files:
            res.append(checkout(f'ls {FOLDER_FOLDER}', i))
        assert all(res), "test2 FAIL"

    def test_step3(self):
        # test3
        assert checkout(f'cd {OUT_FOLDER}; 7z t arx2.{ARC_TYPE}', TEXT_OK), "test3 FAIL"

    def test_step4(self):
        # test4
        res = checkout(f'cd {TST_FOLDER}; 7z u arx2.{ARC_TYPE}', TEXT_OK)
        assert res, "test4 FAIL"

    def test_step5(self, clean_folder, make_files):
        # test5
        res = []
        res.append(checkout(f'cd {TST_FOLDER}; 7z a -t{ARC_TYPE} {OUT_FOLDER}/arx2', TEXT_OK))
        for i in make_files:
            res.append(checkout(f'cd {OUT_FOLDER}; 7z l arx2.{ARC_TYPE}', i))
        assert all(res), "test5 FAIL"

    def test_step6(self, clean_folder, make_files, make_subfolder):
        # test6
        res = []
        res.append(checkout(f'cd {TST_FOLDER}; 7z a -t{ARC_TYPE} {OUT_FOLDER}/arx', TEXT_OK))
        res.append(checkout(f'cd {OUT_FOLDER}; 7z x arx.{ARC_TYPE} -o{FOLDER_FOLDER} -y', TEXT_OK))
        for i in make_files:
            res.append(checkout(f'ls {FOLDER_FOLDER}', i))
        res.append(checkout(f'ls {FOLDER_FOLDER}', make_subfolder[0]))
        res.append(checkout(f'ls {FOLDER_FOLDER}/{make_subfolder[0]}', make_subfolder[1]))
        assert all(res), "test6 FAIL"

    def test_step7(self):
        # test7
        assert checkout(f'cd {OUT_FOLDER}; 7z d arx.{ARC_TYPE}', TEXT_OK), "test7 FAIL"

    def test_step8(self, clean_folder, make_files):
        # test8
        res = []
        for i in make_files:
            res.append(checkout(f'cd {TST_FOLDER}; 7z h {i}', TEXT_OK))
            hash = getout(f'cd {TST_FOLDER}; crc32 {i}').upper()
            res.append(checkout(f'cd {TST_FOLDER}; 7z h {i}', hash))
        assert all(res), "test8 FAIL"
