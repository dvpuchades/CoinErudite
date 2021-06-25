# echarle un vistazo en un futuro para crear un sistema de gestion de las diferentes
# versiones de los modelos de redes neuronales tanto en base a su arquitectura como a 
# su conocimiento


class Training:
    def __init__(self, nn_name, training_iterations, test_iterations):
        self.nn_name = nn_name
        self.product = None
        self.training_iterations = training_iterations
        self.test_iterations = test_iterations
        self.avg_success = -1     # success percentage on a classifier
        self.avg_error = -1       # average error on a predictor
    
    def set_product(self, product_name):
        self.product = product_name

    def set_avg_success(self, avg_success):
        self.avg_success = avg_success
    
    def set_avg_error(self, avg_error):
        self.avg_error = avg_error

    def to_dict(self):
        return {
            'nn_name': str(self.nn_name),
            'product': str(self.product),
            'training_iterations': int(self.training_iterations),
            'test_iterations': int(self.test_iterations),
            'avg_success': float(self.avg_success),
            'avg_error': float(self.avg_error)
        }