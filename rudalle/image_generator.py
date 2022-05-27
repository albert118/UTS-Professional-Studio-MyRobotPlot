import ruclip
import translators
from rudalle.pipelines import generate_images, show, super_resolution, cherry_pick_by_ruclip
from rudalle import get_rudalle_model, get_tokenizer, get_vae, get_realesrgan
from rudalle.utils import seed_everything
import os


def simple_detect_lang(text):
    if len(set('абвгдежзийклмнопрстуфхцчшщъыьэюяё').intersection(text.lower())) > 0:
        return 'ru'
    if len(set('abcdefghijklmnopqrstuvwxyz').intersection(text.lower())) > 0:
        return 'en'
    return 'other'


def get_image(plot, title):
    # prepare models:
    device = 'cuda'
    dalle = get_rudalle_model('Malevich', pretrained=True, fp16=True, device=device)
    tokenizer = get_tokenizer()
    vae = get_vae(dwt=True).to(device)
    # pipeline utils:
    realesrgan = get_realesrgan('x2', device=device)
    clip, processor = ruclip.load('ruclip-vit-base-patch32-384', device=device)
    clip_predictor = ruclip.Predictor(clip, processor, device, bs=8)

    # markdown do not use the English text for inference, you should use translation to Russian,
    # or you can use directly Russian text

    text = plot  # @param

    # markdown *радуга на фоне ночного города / rainbow on the background of the city at night*

    if simple_detect_lang(text) != 'ru':
        text = translators.google(text, from_language='en', to_language='ru')

    print('text:', text)


    seed_everything(42)
    pil_images = []
    scores = []
    for top_k, top_p, images_num in [
        (2048, 0.995, 24),
    ]:
        _pil_images, _scores = generate_images(text, tokenizer, dalle, vae, top_k=top_k, images_num=images_num, bs=8, top_p=top_p)
        pil_images += _pil_images
        scores += _scores

    # i = 0
    # for image in pil_images:
    #     i += 1
    #     image.save(text[:10] + str(i) + "_output.jpg")

    top_images, clip_scores = cherry_pick_by_ruclip(pil_images, text, clip_predictor, count=6)

    sr_images = super_resolution(top_images, realesrgan)
    # show(sr_images, 3)

    path = title.replace(' ', '_')

    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

    i=0
    for image in sr_images:
        i += 1
        image.save(path + '/' + path + str(i) + "_sr_output.jpg")

    top_images, clip_scores = cherry_pick_by_ruclip(sr_images, text, clip_predictor, count=6)

    print(clip_scores)
    return top_images, clip_scores

if __name__ == "__main__":
    plot = "magic spell"
    title = plot
    get_image(plot, title)