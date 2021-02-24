def my_model_passage(sentences):
    from fastNLP.io.loader.conll import CNNERLoader
    data_bundle = CNNERLoader().load("data/")

    from fastNLP.io.pipe.conll import _CNNERPipe
    data_bundle = _CNNERPipe(encoding_type='bio').process(data_bundle)

    src_vocab=data_bundle.get_vocab('chars')
    tgt_vocab=data_bundle.get_vocab('target')

    for i in range(0,27):
        data_bundle.get_dataset('test').delete_instance(0)



    #至此数据处理完毕，两个词典也构建完成
    #构建新的dataset

    from fastNLP import Instance

    for i in range(0,len(sentences)):
        my_raw_chars=[]
        my_target=[]
        my_words=[]
        for j in range(0,len(sentences[i])):
            my_raw_chars.append(sentences[i][j])
            my_target.append(0)
            my_words.append(src_vocab.to_index(sentences[i][j]))

        my_seq_len=len(sentences[i])

        ins=Instance()

        ins.add_field('raw_chars',my_raw_chars)
        ins.add_field('target',my_target)
        ins.add_field('chars',my_words)
        ins.add_field('seq_len',my_seq_len)

        data_bundle.get_dataset('test').append(ins)

    data_bundle.get_dataset('test').delete_instance(0)


    #加载模型
    from fastNLP.io import ModelLoader

    loader=ModelLoader()

    model=loader.load_pytorch_model("./save/bilstmcrf_sec_ner.pkl")

    data_bundle.get_dataset('test').rename_field('chars', 'words')  # 这是由于BiLSTMCRF模型的forward函数接受的words，而不是chars，所以需要把这一列重新命名


    from fastNLP import SpanFPreRecMetric
    metric = SpanFPreRecMetric(tag_vocab=data_bundle.get_vocab('target'))

    #进行测试
    from fastNLP import Tester

    tester = Tester(data_bundle.get_dataset('test'), model, metrics=metric)

    final=tester.get_pred()

    output=''
    labels=[]
    #我们要的是final所有内容
    #原test有两个batch 数目为16 12
    for i in range(0,len(final)):
        for j in range(0,len(final[i])):
            my_label=[]
            for item in final[i][j]:
                my_label.append(tgt_vocab.to_word(item.cpu().item()))
            labels.append(my_label)

    print(labels[0])
    print(final[0][0])
 
    for i in range(0,len(sentences)):
        for j in range(0,len(sentences[i])):
            output=output+sentences[i][j]+' '+labels[i][j]+'\n'

        output=output+'\n'
    return output



def my_model_single_sentence(sentence):
    '''
    #取出Pipe的处理过程，目的是取得由训练集所构建的词典
    from fastNLP.io import WeiboNERLoader

    #load原始数据
    data_bundle = WeiboNERLoader().load()

    #这里需要获取原始数据的此表Vocabulary
    from fastNLP import Vocabulary
    from fastNLP.core.utils import iob2, iob2bioes
    from fastNLP.core.const import Const

    #encoding_type
    encoding_type: str = 'bio'

    if encoding_type == 'bio':
        convert_tag = iob2
    elif encoding_type == 'bioes':
        convert_tag = lambda words: iob2bioes(iob2(words))


    #转换tag
    for name, dataset in data_bundle.datasets.items():
        dataset.apply_field(convert_tag, field_name=Const.TARGET, new_field_name=Const.TARGET)    
   
    #复制一列chars
    data_bundle.copy_field(field_name=Const.RAW_CHAR, new_field_name=Const.CHAR_INPUT, ignore_miss_dataset=True)


    input_field_names = [Const.CHAR_INPUT]
    target_field_names=Const.TARGET

    if isinstance(input_field_names, str):
        input_field_names = [input_field_names]
    if isinstance(target_field_names, str):
        target_field_names = [target_field_names]

    #构建词表
    for input_field_name in input_field_names:
        src_vocab = Vocabulary()
        src_vocab.from_dataset(*[ds for name, ds in data_bundle.iter_datasets() if 'train' in name],
                                field_name=input_field_name,
                                no_create_entry_dataset=[ds for name, ds in data_bundle.iter_datasets()
                                                        if ('train' not in name) and (ds.has_field(input_field_name))]
                                )
        src_vocab.index_dataset(*data_bundle.datasets.values(), field_name=input_field_name)
        data_bundle.set_vocab(src_vocab, input_field_name)
  
    #构建target表
    for target_field_name in target_field_names:
        tgt_vocab = Vocabulary(unknown=None, padding=None)
        tgt_vocab.from_dataset(*[ds for name, ds in data_bundle.iter_datasets() if 'train' in name],
                                field_name=target_field_name,
                                no_create_entry_dataset=[ds for name, ds in data_bundle.iter_datasets()
                                                        if ('train' not in name) and (ds.has_field(target_field_name))]
                                )
        if len(tgt_vocab._no_create_word) > 0:
            warn_msg = f"There are {len(tgt_vocab._no_create_word)} `{target_field_name}` labels" \
                        f" in {[name for name in data_bundle.datasets.keys() if 'train' not in name]} " \
                        f"data set but not in train data set!.\n" \
                        f"These label(s) are {tgt_vocab._no_create_word}"
            warnings.warn(warn_msg)
            logger.warning(warn_msg)
        tgt_vocab.index_dataset(*[ds for ds in data_bundle.datasets.values() if ds.has_field(target_field_name)], field_name=target_field_name)
        data_bundle.set_vocab(tgt_vocab, target_field_name)

    input_fields = [Const.TARGET, Const.INPUT_LEN] + input_field_names
    target_fields = [Const.TARGET, Const.INPUT_LEN]
        
    for name, dataset in data_bundle.datasets.items():
        dataset.add_seq_len(Const.CHAR_INPUT)
        
    data_bundle.set_input(*input_fields)
    data_bundle.set_target(*target_fields)
    '''
    '''
    from fastNLP.io import WeiboNERPipe
    data_bundle = WeiboNERPipe().process_from_file()
    '''
    from fastNLP.io.loader.conll import CNNERLoader
    data_bundle = CNNERLoader().load("data/")

    from fastNLP.io.pipe.conll import _CNNERPipe
    data_bundle = _CNNERPipe(encoding_type='bio').process(data_bundle)

    src_vocab=data_bundle.get_vocab('chars')
    tgt_vocab=data_bundle.get_vocab('target')

    #至此数据处理完毕，两个词典也构建完成
    #需要增加数据的是data_bundle.get_dataset('test')这一个fastNLP dataset对象
    #该数据结构格式为 raw_chars target chars seq_len

    from fastNLP import Instance

    my_raw_chars=[]
    my_target=[]
    my_words=[]
    for i in range(0,len(sentence)):
        my_raw_chars.append(sentence[i])
        my_target.append(0)
        my_words.append(src_vocab.to_index(sentence[i]))

    my_seq_len=len(sentence)

    ins=Instance()

    ins.add_field('raw_chars',my_raw_chars)
    ins.add_field('target',my_target)
    ins.add_field('chars',my_words)
    ins.add_field('seq_len',my_seq_len)

    data_bundle.get_dataset('test').append(ins)

    #加载模型
    from fastNLP.io import ModelLoader

    loader=ModelLoader()

    model=loader.load_pytorch_model("./save/bilstmcrf_sec_ner.pkl")

    data_bundle.rename_field('chars', 'words')  # 这是由于BiLSTMCRF模型的forward函数接受的words，而不是chars，所以需要把这一列重新命名

    from fastNLP import SpanFPreRecMetric
    metric = SpanFPreRecMetric(tag_vocab=data_bundle.get_vocab('target'))

    #进行测试
    from fastNLP import Tester

    tester = Tester(data_bundle.get_dataset('test'), model, metrics=metric)

    final=tester.get_pred()

    my_label=[]
    #我们要的是final的最后一个的最后一行
    for i in final[len(final)-1][len(final[len(final)-1])-1]:
        i=i.cpu().item()
        my_label.append(tgt_vocab.to_word(i))

    output=''
    for j in range(0,my_seq_len):
        output=output+sentence[j]+' '+my_label[j]+'\n'

    return output

'''
##用于测试test中原本的数目
from fastNLP.io.loader.conll import CNNERLoader
data_bundle = CNNERLoader().load("data/")

from fastNLP.io.pipe.conll import _CNNERPipe
data_bundle = _CNNERPipe(encoding_type='bio').process(data_bundle)

src_vocab=data_bundle.get_vocab('chars')
tgt_vocab=data_bundle.get_vocab('target')

#至此数据处理完毕，两个词典也构建完成
#构建新的dataset

#加载模型
from fastNLP.io import ModelLoader

loader=ModelLoader()

model=loader.load_pytorch_model("./save/bilstmcrf_sec_ner.pkl")

data_bundle.get_dataset('test').rename_field('chars', 'words')  # 这是由于BiLSTMCRF模型的forward函数接受的words，而不是chars，所以需要把这一列重新命名


from fastNLP import SpanFPreRecMetric
metric = SpanFPreRecMetric(tag_vocab=data_bundle.get_vocab('target'))

#进行测试
from fastNLP import Tester

tester = Tester(data_bundle.get_dataset('test'), model, metrics=metric)

final=tester.get_pred()

print(len(final))
for i in range(0,len(final)):
    print(len(final[i]))
'''