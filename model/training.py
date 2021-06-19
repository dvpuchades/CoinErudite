# echarle un vistazo en un futuro para crear un sistema de gestion de las diferentes
# versiones de los modelos de redes neuronales tanto en base a su arquitectura como a 
# su conocimiento


class training:
    def __init__(self, first_data, last_data, first_test_data, last_test_data):
        self.product = None
        self.first_data = first_data
        self.last_data = last_data
        self.first_test_data = first_test_data
        self.last_test_data = last_test_data
        self.training_iterations = last_data - first_data
        self.test_iterations = last_test_data - first_test_data
        self.avg_success = None
        self.avg_error = None
    
    def set_product(self, product_name):
        self.product = product_name

    def set_avg_success(self, avg_success):
        self.avg_success = avg_success
    
    def set_avg_error(self, avg_error):
        self.avg_error = avg_error

    def to_dict(self):
        return {
            'product': self.product,
            'first_data': self.first_data, 
            'last_data': self.last_data,
            'first_test_data': self.first_test_data,
            'last_test_data': self.last_test_data,
            'training_iterations': self.training_iterations,
            'test_iterations': self.test_iterations,
            'avg_success': self.avg_success,
            'avg_error': self.avg_error
        }