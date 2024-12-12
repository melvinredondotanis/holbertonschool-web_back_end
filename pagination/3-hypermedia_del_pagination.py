#!/usr/bin/env python3
""" Main file """

import csv
from math import ceil
from typing import List, Tuple, Dict


index_range = __import__('0-simple_helper_function').index_range


class Server:
    """
    Server class to paginate a database of popular baby names
    """

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """
        Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Get the page

        Args:
            page: Current page
            page_size: Total size of the page

        Return:
            List of the pagination done
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        range = index_range(page, page_size)
        pagination = self.dataset()

        return (pagination[range[0]:range[1]])

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """
        Get the hypermedia pagination
        Args:
            page: Current page
            page_size: Total size of the page
        Return:
            Dict with the pagination data
        """

        data = []
        try:
            data = self.get_page(page, page_size)
        except AssertionError:
            return {}

        dataset = self.dataset()
        totalpag = len(dataset) if dataset else 0
        totalpag = ceil(totalpag / page_size)
        prevpag = (page - 1) if (page - 1) >= 1 else None
        nextpag = (page + 1) if (page + 1) <= totalpag else None

        hypermedia = {
            'page_size': page_size,
            'page': page,
            'data': data,
            'next_page': nextpag,
            'prev_page': prevpag,
            'total_pages': totalpag,
        }

        return hypermedia

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Get the hypermedia pagination with index
        Args:
            index: Current index
            page_size: Total size of the page
        Return:
            Dict with the pagination data
        """

        result_dataset = []
        index_data = self.indexed_dataset()
        keys_list = list(index_data.keys())
        assert index + page_size < len(keys_list)
        assert index < len(keys_list)

        if index not in index_data:
            start_index = keys_list[index]
        else:
            start_index = index

        for i in range(start_index, start_index + page_size):
            if i not in index_data:
                result_dataset.append(index_data[keys_list[i]])
            else:
                result_dataset.append(index_data[i])

        next_index = index + page_size

        if index in keys_list:
            next_index
        else:
            next_index = keys_list[next_index]

        return {
            'index': index,
            'next_index': next_index,
            'page_size': len(result_dataset),
            'data': result_dataset
        }
