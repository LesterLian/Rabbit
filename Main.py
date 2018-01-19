# -*- coding: utf-8 -*-
# @Author  : Lester
import Control
import global_var

infoList = global_var.passport_list  # Should be passed in by UI
if __name__ == '__main__':
    Control.init(infoList)
    Control.process()
