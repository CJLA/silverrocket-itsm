import {
  useState,
  type ChangeEvent,
  type SubmitEvent,
} from "react";

import {
  registerUser,
  type ApiValidationErrors,
  type RegisterUserRequest,
} from "../../services/users";

interface RegisterUserFormValues extends RegisterUserRequest {
  confirmPassword: string;
}

type FormErrors = Partial<
  Record<keyof RegisterUserFormValues, string>
> & {
  general?: string;
};

const initialFormValues: RegisterUserFormValues = {
  first_name: "",
  last_name: "",
  email: "",
  password: "",
  confirmPassword: "",
};

function CreateUserPage() {
  const [formValues, setFormValues] =
    useState<RegisterUserFormValues>(initialFormValues);

  const [formErrors, setFormErrors] = useState<FormErrors>({});
  const [successMessage, setSuccessMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;

    setFormValues((prevValues) => ({
      ...prevValues,
      [name]: value,
    }));

    setFormErrors((currentErrors) => ({
      ...currentErrors,
      [name]: undefined,
      general: undefined,
    }));

    setSuccessMessage("");
  };

  function validateForm(): FormErrors {
    const validationErrors: FormErrors = {};

    if (!formValues.first_name.trim()) {
      validationErrors.first_name = "First name is required.";
    }

    if (!formValues.last_name.trim()) {
      validationErrors.last_name = "Last name is required.";
    }

    if (!formValues.email.trim()) {
      validationErrors.email = "Email is required.";
    } else if (!/\S+@\S+\.\S+/.test(formValues.email)) {
      validationErrors.email = "Invalid email format.";
    }

    if (!formValues.password) {
      validationErrors.password = "Password is required.";
    } else if (formValues.password.length < 8) {
      validationErrors.password =
        "Password must be at least 8 characters long.";
    }

    if (!formValues.confirmPassword) {
      validationErrors.confirmPassword =
        "Please confirm the password.";
    } else if (
      formValues.password !== formValues.confirmPassword
    ) {
      validationErrors.confirmPassword =
        "Passwords do not match.";
    }

    return validationErrors;
  }

  function convertApiErrors(
    apiErrors: ApiValidationErrors,
  ): FormErrors {
    const convertedErrors: FormErrors = {};

    for (const [field, messages] of Object.entries(apiErrors)) {
      const message = Array.isArray(messages)
        ? messages.join(" ")
        : String(messages);

      if (field in initialFormValues) {
        convertedErrors[
          field as keyof RegisterUserFormValues
        ] = message;
      } else {
        convertedErrors.general = message;
      }
    }

    return convertedErrors;
  }

  const handleSubmit = async (
    e: SubmitEvent<HTMLFormElement>,
  ) => {
    e.preventDefault();

    const validationErrors = validateForm();

    if (Object.keys(validationErrors).length > 0) {
      setFormErrors(validationErrors);
      return;
    }

    setIsSubmitting(true);
    setFormErrors({});
    setSuccessMessage("");

    try {
      await registerUser({
        first_name: formValues.first_name.trim(),
        last_name: formValues.last_name.trim(),
        email: formValues.email.trim(),
        password: formValues.password,
      });

      setSuccessMessage(
        `User ${formValues.email.trim()} was created successfully.`,
      );

      setFormValues(initialFormValues);
    } catch (error: unknown) {
      if (error && typeof error === "object") {
        setFormErrors(
          convertApiErrors(error as ApiValidationErrors),
        );
      } else {
        setFormErrors({
          general:
            "The user could not be created. Please try again.",
        });
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCancel = () => {
    setFormValues(initialFormValues);
    setFormErrors({});
    setSuccessMessage("");
  };

  return (
    <main className="register-page">
    <div className="register-page_content">
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-12 col-md-8 col-lg-6 col-xl-5">
            <h1 className="h2 mb-4 text-center">
              Register New User
            </h1>

            {successMessage && (
              <div className="alert alert-success" role="alert">
                {successMessage}
              </div>
            )}

            {formErrors.general && (
              <div className="alert alert-danger" role="alert">
                {formErrors.general}
              </div>
            )}

            <form onSubmit={handleSubmit} noValidate>
              <div className="mb-4">
                <label
                  className="form-label"
                  htmlFor="first_name"
                >
                  First Name
                </label>

                <input
                  className={`form-control ${
                    formErrors.first_name ? "is-invalid" : ""
                  }`}
                  id="first_name"
                  name="first_name"
                  type="text"
                  value={formValues.first_name}
                  onChange={handleChange}
                  autoComplete="given-name"
                />

                {formErrors.first_name && (
                  <div className="invalid-feedback">
                    {formErrors.first_name}
                  </div>
                )}
              </div>

              <div className="mb-4">
                <label
                  className="form-label"
                  htmlFor="last_name"
                >
                  Last Name
                </label>

                <input
                  className={`form-control ${
                    formErrors.last_name ? "is-invalid" : ""
                  }`}
                  id="last_name"
                  name="last_name"
                  type="text"
                  value={formValues.last_name}
                  onChange={handleChange}
                  autoComplete="family-name"
                />

                {formErrors.last_name && (
                  <div className="invalid-feedback">
                    {formErrors.last_name}
                  </div>
                )}
              </div>

              <div className="mb-4">
                <label className="form-label" htmlFor="email">
                  Email Address
                </label>

                <input
                  className={`form-control ${
                    formErrors.email ? "is-invalid" : ""
                  }`}
                  id="email"
                  name="email"
                  type="email"
                  value={formValues.email}
                  onChange={handleChange}
                  autoComplete="email"
                />

                {formErrors.email && (
                  <div className="invalid-feedback">
                    {formErrors.email}
                  </div>
                )}
              </div>

              <div className="mb-4">
                <label
                  className="form-label"
                  htmlFor="password"
                >
                  Password
                </label>

                <input
                  className={`form-control ${
                    formErrors.password ? "is-invalid" : ""
                  }`}
                  id="password"
                  name="password"
                  type="password"
                  value={formValues.password}
                  onChange={handleChange}
                  autoComplete="new-password"
                />

                <div className="form-text text-start">
                  Password must be at least 8 characters long.
                </div>

                {formErrors.password && (
                  <div className="invalid-feedback">
                    {formErrors.password}
                  </div>
                )}
              </div>

              <div className="mb-5">
                <label
                  className="form-label"
                  htmlFor="confirmPassword"
                >
                  Confirm Password
                </label>

                <input
                  className={`form-control ${
                    formErrors.confirmPassword
                      ? "is-invalid"
                      : ""
                  }`}
                  id="confirmPassword"
                  name="confirmPassword"
                  type="password"
                  value={formValues.confirmPassword}
                  onChange={handleChange}
                  autoComplete="new-password"
                />

                <div className="form-text text-start">
                  Enter the same password as before, for verification.
                </div>

                {formErrors.confirmPassword && (
                  <div className="invalid-feedback">
                    {formErrors.confirmPassword}
                  </div>
                )}
              </div>

              <div className="d-flex gap-2">
                <button
                  className="btn btn-primary me-2"
                  type="submit"
                  disabled={isSubmitting}
                >
                  {isSubmitting
                    ? "Creating User..."
                    : "Register User"}
                </button>

                <button
                  className="btn btn-outline-secondary"
                  type="button"
                  onClick={handleCancel}
                  disabled={isSubmitting}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </main>
  );
}

export default CreateUserPage;