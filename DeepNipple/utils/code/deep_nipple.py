from fastai.vision import *
import cv2

from utils.code.aux_func import seg2bbox, predict

def DeepNipple(image_path, learner_path, alg_mode, show=True):
    '''
    :param image_path: input image absolute path
    :param alg_mode: seg/bbox
    :param device: cpu or gpu number
    :return: segmentation mask / bounding boxes
    '''

    # load pyrtoch model
    learner = load_learner(learner_path)

    image, mask = predict(image_path, learner)
    print(image.shape, mask.shape)

    # bounding box coordinates
    coords = seg2bbox(mask)

    if alg_mode == 'seg':

        output = mask

        plt.subplot(121)
        plt.imshow(image)
        plt.title('Original image')
        plt.axis('off')
        plt.subplot(122)
        plt.imshow(image)
        plt.axis('off')
        plt.imshow(mask[:, :, 1], alpha=0.6, interpolation='bilinear', cmap='magma')
        plt.axis('off')
        plt.imshow(mask[:, :, 2], alpha=0.6, interpolation='bilinear', cmap='afmhot')
        plt.axis('off')
        plt.title('NAC segmentation')
        plt.show()

    else:
        output = []  # a list of coordinates (numpy array)
        # compute the center of the bounding boxes
        for coor in coords:
            y1, y2, x1, x2 = coor[0], coor[1], coor[2], coor[3]
            cv2.rectangle(image, (x1, y1), (x2, y2), (36, 255, 12), 2, -1)
            center = np.array([(x1+x2)/2, (y1+y2)/2])
            output.append(center)
        output = np.vstack(output)

        if show:
            plt.imshow(image)
            plt.show()

    return output, image