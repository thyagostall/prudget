<?php

namespace AppBundle\Controller;

use AppBundle\Entity\Account;
use Doctrine\ORM\EntityManager;
use Sensio\Bundle\FrameworkExtraBundle\Configuration\Route;
use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\Form\Extension\Core\Type\SubmitType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\HttpFoundation\Request;

class AccountController extends Controller
{
    /** @var EntityManager */
    private $entityManager;

    /**
     * DefaultController constructor.
     * @param EntityManager $entityManager
     */
    public function __construct(EntityManager $entityManager)
    {
        $this->entityManager = $entityManager;
    }

    /**
     * @Route("/account", name="new-account")
     */
    public function newAccount(Request $request)
    {
        $account = new Account();
        $account->setBalance(0);

        $form = $this->createFormBuilder($account)
            ->add('name', TextType::class)
            ->add('submit', SubmitType::class)
            ->getForm();

        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $this->entityManager->persist($account);
            $this->entityManager->flush();

            return $this->redirectToRoute('accounts');
        }

        return $this->render('account/new-edit.html.twig', [
            'form' => $form->createView()
        ]);
    }

    /**
     * @Route("/account/edit/{id}", name="edit-account")
     */
    public function editAccount(Request $request)
    {
        $id = $request->get('id');
        $account = $this->entityManager
            ->getRepository(Account::class)
            ->find($id);

        if (!$account) {
            throw $this->createNotFoundException();
        }

        $form = $this->createFormBuilder($account)
            ->add('name', TextType::class)
            ->add('submit', SubmitType::class)
            ->getForm();

        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $this->entityManager->persist($account);
            $this->entityManager->flush();

            return $this->redirectToRoute('accounts');
        }

        return $this->render('account/new-edit.html.twig', [
            'form' => $form->createView()
        ]);
    }

    /**
     * @Route("/account/delete/{id}", name="delete-account")
     */
    public function deleteAccount(Request $request)
    {
        $id = $request->get('id');
        $account = $this->entityManager
            ->getRepository(Account::class)
            ->find($id);

        if (!$account) {
            throw $this->createNotFoundException();
        }

        $this->entityManager->remove($account);
        $this->entityManager->flush();

        return $this->redirectToRoute('accounts');
    }

    /**
     * @Route("/accounts", name="accounts")
     */
    public function accounts(Request $request)
    {
        $repository = $this->entityManager->getRepository(Account::class);
        $accounts = $repository->findAll();

        return $this->render('account/index.html.twig', [
            'accounts' => $accounts
        ]);
    }
}