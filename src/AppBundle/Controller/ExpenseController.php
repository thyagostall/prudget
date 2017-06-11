<?php

namespace AppBundle\Controller;


use AppBundle\Entity\Expense;
use Doctrine\ORM\EntityManager;
use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\Form\Extension\Core\Type\IntegerType;
use Symfony\Component\Form\Extension\Core\Type\MoneyType;
use Symfony\Component\Form\Extension\Core\Type\SubmitType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;

class ExpenseController extends Controller
{
    private $entityManager;

    /**
     * ExpenseController constructor.
     * @param $entityManager
     */
    public function __construct(EntityManager $entityManager)
    {
        $this->entityManager = $entityManager;
    }

    /**
     * @Route("/expenses", name="expenses")
     */
    public function expenses(Request $request)
    {
        $repository = $this->entityManager->getRepository(Expense::class);
        $expenses = $repository->findAll();

        return $this->render('expense/index.html.twig', [
            'expenses' => $expenses
        ]);
    }

    /**
     * @Route("/expense", name="new-expense")
     */
    public function newExpense(Request $request)
    {
        $expense = new Expense();

        $form = $this->createFormBuilder($expense)
            ->add('name', TextType::class)
            ->add('day', IntegerType::class)
            ->add('value', MoneyType::class)
            ->add('submit', SubmitType::class)
            ->getForm();

        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $this->entityManager->persist($expense);
            $this->entityManager->flush();

            return $this->redirectToRoute('expenses');
        }

        return $this->render('expense/new-edit.html.twig', [
            'form' => $form->createView()
        ]);
    }

    /**
     * @Route("/expense/edit/{id}", name="edit-expense")
     */
    public function editExpense(Request $request)
    {
        $id = $request->get('id');

        $repository = $this->entityManager->getRepository(Expense::class);
        $expense = $repository->find($id);

        if (!$expense) {
            throw $this->createNotFoundException();
        }

        $form = $this->createFormBuilder($expense)
            ->add('name', TextType::class)
            ->add('day', IntegerType::class)
            ->add('value', MoneyType::class)
            ->add('submit', SubmitType::class)
            ->getForm();

        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $this->entityManager->persist($expense);
            $this->entityManager->flush();

            return $this->redirectToRoute('expenses');
        }

        return $this->render('expense/new-edit.html.twig', [
            'form' => $form->createView()
        ]);
    }

    /**
     * @Route("/expense/delete/{id}", name="delete-expense")
     */
    public function deleteExpense(Request $request)
    {
        $id = $request->get('id');

        $repository = $this->entityManager->getRepository(Expense::class);
        $expense = $repository->find($id);

        if (!$expense) {
            throw $this->createNotFoundException();
        }

        $this->entityManager->remove($expense);
        $this->entityManager->flush();

        return $this->redirectToRoute('expenses');
    }

}