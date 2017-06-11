<?php

namespace AppBundle\Controller;


use AppBundle\Entity\Category;
use Doctrine\ORM\EntityManager;
use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Sensio\Bundle\FrameworkExtraBundle\Configuration\Route;
use Symfony\Component\Form\Extension\Core\Type\SubmitType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\HttpFoundation\Request;

class CategoryController extends Controller
{
    /** @var EntityManager */
    private $entityManager;

    /**
     * CategoryController constructor.
     * @param EntityManager $entityManager
     */
    public function __construct(EntityManager $entityManager)
    {
        $this->entityManager = $entityManager;
    }

    /**
     * @Route("/category", name="new-category")
     */
    public function newCategory(Request $request)
    {
        $category = new Category();
        $category->setBalance(0);

        $form = $this->createFormBuilder($category)
            ->add('name', TextType::class)
            ->add('submit', SubmitType::class)
            ->getForm();

        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $this->entityManager->persist($category);
            $this->entityManager->flush();

            return $this->redirectToRoute('categories');
        }

        return $this->render('category/new-edit.html.twig', [
            'form' => $form->createView()
        ]);
    }

    /**
     * @Route("/category/edit/{id}", name="edit-category")
     */
    public function editCategory(Request $request)
    {
        $id = $request->get('id');

        $category = $this->entityManager
            ->getRepository(Category::class)
            ->find($id);

        if (!$category) {
            throw $this->createNotFoundException();
        }

        $form = $this->createFormBuilder($category)
            ->add('name', TextType::class)
            ->add('submit', SubmitType::class)
            ->getForm();

        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $this->entityManager->persist($category);
            $this->entityManager->flush();

            return $this->redirectToRoute('categories');
        }

        return $this->render('category/new-edit.html.twig', [
            'form' => $form->createView()
        ]);
    }

    /**
     * @Route("/category/delete/{id}", name="delete-category")
     */
    public function deleteCategory(Request $request)
    {
        $id = $request->get('id');

        $category = $this->entityManager
            ->getRepository(Category::class)
            ->find($id);

        if (!$category) {
            throw $this->createNotFoundException();
        }

        $this->entityManager->remove($category);
        $this->entityManager->flush();

        return $this->redirectToRoute('categories');
    }

    /**
     * @Route("/categories", name="categories")
     */
    public function categories(Request $request)
    {
        $repository = $this->entityManager->getRepository(Category::class);
        $categories = $repository->findAll();

        return $this->render('category/index.html.twig', [
            'categories' => $categories
        ]);
    }
}