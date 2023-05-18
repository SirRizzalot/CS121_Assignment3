from Retrieval import load_data


if __name__ ==  "__main__":
    url_data = load_data('url_ids.csv', ',')
    word_data = load_data('word_index_locator.csv', ',')

    print("URL Data:")
    print(url_data)
    print("\nWord Data:")
    print(word_data)