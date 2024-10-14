class ModelProcessor:
    def __init__(self, process_type, target_column, ignore_columns, file_name):
        self.process_type = process_type
        self.target_column = target_column
        self.ignore_columns = ignore_columns
        self.file_name = file_name
        self.data = None

    def process(self):
        try:
            if self.process_type == 'classification':
                return self._process_classification()
            elif self.process_type == 'regression':
                return self._process_regression()
            elif self.process_type == 'time-series':
                return self._process_time_series()
            else:
                raise ValueError("Tipo de procesamiento no válido.")
        except ValueError as ve:
            print(f"Error de valor: {ve}")
        except Exception as e:
            print(f"Ha ocurrido un error: {e}")

    def _process_classification(self):
        try:
            from pycaret.classification import setup, compare_models, tune_model
            from pycaret.datasets import get_data

            # Cargar datos
            self.data = get_data(self.file_name)
            if self.target_column not in self.data.columns:
                raise KeyError(f"La columna objetivo '{self.target_column}' no se encuentra en los datos.")

            # Setup de clasificación
            setup(data=self.data, 
                  target=self.target_column, 
                  ignore_features=self.ignore_columns, 
                  normalize=True, 
                  remove_outliers=True)

            # Comparar y ajustar modelo
            best_model = compare_models(sort="Accuracy")
            tuned_model = tune_model(best_model)
            return tuned_model

        except KeyError as ke:
            print(f"Error: {ke}")
        except Exception as e:
            print(f"Error durante el procesamiento de clasificación: {e}")

    def _process_regression(self):
        try:
            from pycaret.regression import setup, compare_models, tune_model
            from pycaret.datasets import get_data

            # Cargar datos
            self.data = get_data(self.file_name)
            if self.target_column not in self.data.columns:
                raise KeyError(f"La columna objetivo '{self.target_column}' no se encuentra en los datos.")

            # Setup de regresión
            setup(data=self.data, 
                  target=self.target_column, 
                  ignore_features=self.ignore_columns, 
                  normalize=True, 
                  transformation=True, 
                  remove_outliers=True, 
                  remove_multicollinearity=True, 
                  imputation_type='iterative')

            # Comparar y ajustar modelo
            best_model = compare_models(sort="MAE")
            tuned_model = tune_model(best_model)
            return tuned_model

        except KeyError as ke:
            print(f"Error: {ke}")
        except Exception as e:
            print(f"Error durante el procesamiento de regresión: {e}")

    def _process_time_series(self):
        try:
            from pycaret.time_series import setup, compare_models, tune_model
            from pycaret.datasets import get_data

            # Cargar datos
            self.data = get_data(self.file_name)
            if self.target_column not in self.data.columns:
                raise KeyError(f"La columna objetivo '{self.target_column}' no se encuentra en los datos.")

            # Setup de series temporales
            setup(self.data[self.target_column], fh=1)

            # Comparar y ajustar modelo
            best_model = compare_models()
            tuned_model = tune_model(best_model)
            return tuned_model

        except KeyError as ke:
            print(f"Error: {ke}")
        except Exception as e:
            print(f"Error durante el procesamiento de series temporales: {e}")

# Ejemplo de instancia
# try:
#     processor = ModelProcessor('time-series', 'Outcome', [], 'diabetes')
#     modelo_entrenado = processor.process()
# except Exception as e:
#     print(f"Ha ocurrido un error general: {e}")
