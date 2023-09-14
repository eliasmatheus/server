import { useEffect, useState } from 'react';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { FieldValues, useForm } from 'react-hook-form';

import { Button } from '../components/Buttons/Button';
import { Input } from '../components/Form/Input';
import Header from '../components/Header';
import api from '../services/api';
import { ErrorWarning } from '../components/Form/ErrorWarning';
import { useToast } from '../hooks/toast';
import { GoBackButton } from '../components/Buttons/GoBackButton';

const INITIAL_VALUES = {
  firs_name: '',
  last_name: '',
  email: '',
  twitter_username: '',
  avatar_url: '',
};

function AuthorForm() {
  const navigate = useNavigate();
  const { addToast } = useToast();
  const { id } = useParams();
  const [isSubmitSuccessful, setSubmitSuccessful] = useState(false);
  const [loadingSubmit, setLoadingSubmit] = useState(false);
  const [loadingDelete, setLoadingDelete] = useState(false);

  const [avatarPreview, setAvatarPreview] = useState(null);

  const {
    register,
    handleSubmit,
    reset,
    control,
    watch,
    formState: { errors },
  } = useForm();

  /**
   * UseEffect chamado quando o componente é montado ou quando o pathname muda
   *
   * Se o pathname possuir o parâmetro 'id' o useEffect buscará os dados do
   * author pelo id no backend e preencherá o formulário com os dados.
   * Caso contrário, o useEffect apenas limpará o formulário.
   */
  useEffect(() => {
    if (!id) {
      reset(INITIAL_VALUES);

      return;
    }

    api.get(`/author/${id}`).then(response => {
      reset(response.data);
      setAvatarPreview(response.data.avatar_url);
    });
  }, [useLocation().pathname]);

  /**
   * Função que envia os dados do formulário para o backend.
   *
   * @param data - Dados do formulário
   */
  function handleSaveAuthor(data: FieldValues) {
    const formData = new FormData();

    // Se estiver editando, envia o id do author
    if (id) {
      formData.append('id', id);
    }

    Object.entries(data).forEach(([key, value]) => {
      formData.append(key, value);
    });

    setLoadingSubmit(true);

    // Simula o tempo de espera para a requisição
    setTimeout(() => {
      submitAuthor(formData);
    }, 2000);
  }

  async function submitAuthor(formData: FormData) {
    const method = id ? 'put' : 'post';

    await api[method]('/author', formData)
      .then(response => {
        addToast({
          type: 'success',
          title: `Author ${id ? 'updated' : 'created'} successfully!`,
        });

        setSubmitSuccessful(true);
        setLoadingSubmit(false);

        navigate(`/authors`);
      })
      .catch(error => {
        setLoadingSubmit(false);

        addToast({
          type: 'error',
          title: 'Error creating author!',
          description: 'Please try again',
        });
      });
  }

  /**
   * Função que envia os dados do formulário para o backend.
   *
   * @param data - Dados do formulário
   */
  function handleDeleteAuthor() {
    if (window.confirm('Are you sure you want to delete this author?')) {
      setLoadingDelete(true);

      // Simula o tempo de espera para a requisição
      setTimeout(() => {
        deleteAuthor();
      }, 2000);
    }
  }

  async function deleteAuthor() {
    await api
      .delete(`/author/${id}`)
      .then(response => {
        addToast({
          type: 'success',
          title: `Author deleted successfully!`,
        });

        setSubmitSuccessful(true);
        setLoadingDelete(false);

        navigate(`/authors`);
      })
      .catch(error => {
        setLoadingDelete(false);

        addToast({
          type: 'error',
          title: 'Error creating deleting!',
          description: 'Please try again',
        });
      });
  }

  // Reseta após o submit ser bem sucedido
  useEffect(() => {
    reset(INITIAL_VALUES);
  }, [isSubmitSuccessful]);

  useEffect(() => {
    const subscription = watch((value, { name, type }) => {
      if (name === 'avatar_url') {
        setAvatarPreview(value.avatar_url);
      }
    });
    return () => subscription.unsubscribe();
  }, [watch]);

  return (
    <>
      <Header />

      <div className="max-w-8xl mx-auto">
        <div className="flex px-4 pt-8 pb-10 lg:px-8">
          <GoBackButton />
        </div>
      </div>

      <main className="max-w-[52rem] mx-auto px-4 pb-10 sm:px-6 md:px-8 xl:px-12 lg:max-w-6xl">
        <header>
          <section className="mt-3 max-w-4xl sm:mx-auto sm:px-4">
            <form onSubmit={handleSubmit(handleSaveAuthor)}>
              <div className="space-y-12">
                <div className="border-b border-slate-900/10 dark:border-slate-200/10 pb-12">
                  <h2 className="text-lg font-semibold leading-7 text-slate-900 dark:text-slate-200">
                    Author Information
                  </h2>
                  <p className="mt-1 text-sm leading-6 text-slate-600">
                    Use this form to add a new author
                  </p>

                  <div className="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
                    <div className="sm:col-span-3">
                      <label
                        className="font-semibold block mb-1 required"
                        htmlFor="first_name"
                      >
                        First Name
                      </label>

                      <Input
                        id="first_name"
                        type="text"
                        label="first_name"
                        register={register}
                        required
                        placeholder="First Name"
                      />
                      {errors.first_name && (
                        <ErrorWarning>This field is required</ErrorWarning>
                      )}
                    </div>

                    <div className="sm:col-span-3">
                      <label
                        className="font-semibold block mb-1 required"
                        htmlFor="last_name"
                      >
                        Last Name
                      </label>

                      <Input
                        id="last_name"
                        type="text"
                        label="last_name"
                        register={register}
                        required
                        placeholder="Last Name"
                      />
                      {errors.last_name && (
                        <ErrorWarning>This field is required</ErrorWarning>
                      )}
                    </div>

                    <div className="sm:col-span-3 required">
                      <label
                        className="font-semibold block mb-1"
                        htmlFor="twitter_username"
                      >
                        Email
                      </label>

                      <Input
                        id="email"
                        type="text"
                        label="email"
                        register={register}
                        required
                        placeholder="Email"
                      />
                      {errors.email && (
                        <ErrorWarning>This field is required</ErrorWarning>
                      )}
                    </div>

                    <div className="sm:col-span-3">
                      <label
                        className="font-semibold block mb-1"
                        htmlFor="twitter_username"
                      >
                        Twitter Username
                      </label>

                      <Input
                        id="twitter_username"
                        type="text"
                        label="twitter_username"
                        register={register}
                        placeholder="Twitter Username"
                      />
                      {errors.twitter_username && (
                        <ErrorWarning>This field is required</ErrorWarning>
                      )}
                    </div>

                    <div className="sm:col-span-1">
                      <label className="font-semibold block mb-1" htmlFor="avatar_url">
                        Avatar Preview
                      </label>

                      <div className="w-16 h-16 p-[0.1875rem] rounded-full ring-1 ring-slate-900/10 shadow overflow-hidden flex-none dark:bg-sky-500 dark:highlight-white/20">
                        <div className="aspect-w-1 aspect-h-1 bg-[length:100%]">
                          <img
                            src={avatarPreview || '/images/avatar-placeholder.png'}
                            alt=""
                            className="rounded-full bg-slate-50 dark:bg-slate-800"
                            decoding="async"
                          />
                        </div>
                      </div>
                    </div>
                    <div className="sm:col-span-5">
                      <label className="font-semibold block mb-1" htmlFor="avatar_url">
                        Avatar URL
                      </label>

                      <Input
                        id="avatar_url"
                        type="text"
                        label="avatar_url"
                        register={register}
                        placeholder="Avatar URL"
                      />
                      {errors.avatar_url && (
                        <ErrorWarning>This field is required</ErrorWarning>
                      )}
                    </div>
                  </div>
                </div>

                <div className="mt-6 flex items-center justify-end gap-x-3">
                  <div>
                    <Button
                      type="button"
                      color="alternative"
                      onClick={() => navigate(-1)}
                    >
                      Cancel and go back
                    </Button>
                  </div>

                  {id && (
                    <div>
                      <Button
                        type="button"
                        color="red"
                        onClick={handleDeleteAuthor}
                        loading={loadingDelete}
                      >
                        Delete Author*
                      </Button>
                    </div>
                  )}

                  <div>
                    <Button type="submit" color="default" loading={loadingSubmit}>
                      Save
                    </Button>
                  </div>
                </div>
                {id && (
                  <div className="text-right text-sm">
                    <p>
                      *Deleting an author will result in the deletion of all their
                      articles.
                    </p>
                  </div>
                )}
              </div>
            </form>
          </section>
        </header>
      </main>
    </>
  );
}

export default AuthorForm;
