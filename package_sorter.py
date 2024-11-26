from typing import Union, Optional
import math
import sys
from decimal import Decimal, InvalidOperation

class PackageError(Exception):
    """Custom exception for package-related errors"""
    pass

class Package:
    """Represents a package with validation and sorting logic"""
    
    # Constants for validation and sorting
    MAX_DIMENSION = 1000  # cm
    MAX_MASS = 1000      # kg
    MIN_DIMENSION = sys.float_info.epsilon
    BULKY_VOLUME = 1_000_000  # cm³
    BULKY_DIMENSION = 150     # cm
    HEAVY_MASS = 20          # kg
    
    def __init__(self, width: Union[int, float, str], 
                 height: Union[int, float, str],
                 length: Union[int, float, str], 
                 mass: Union[int, float, str]):
        """
        Initialize a package with given dimensions and mass.
        
        Args:
            width: Width in centimeters
            height: Height in centimeters
            length: Length in centimeters
            mass: Mass in kilograms
            
        Raises:
            PackageError: If any input is invalid
        """
        self.width = self._validate_numeric(width, "width")
        self.height = self._validate_numeric(height, "height")
        self.length = self._validate_numeric(length, "length")
        self.mass = self._validate_numeric(mass, "mass")
        
        # Cache calculations
        self._volume: Optional[float] = None
        self._max_dimension: Optional[float] = None
    
    @staticmethod
    def _validate_numeric(value: Union[int, float, str], param_name: str) -> float:
        """Validate and convert input to float"""
        try:
            # Handle string inputs (including unicode numbers)
            if isinstance(value, str):
                # Remove whitespace and normalize unicode numbers
                value = ''.join(char for char in value if not char.isspace())
                value = Decimal(value)
            
            # Convert to float
            value = float(value)
            
            # Check for special float values
            if math.isnan(value) or math.isinf(value):
                raise PackageError(f"Invalid {param_name}: {value}. Must be a finite number")
            
            # Check bounds
            if value <= Package.MIN_DIMENSION:
                raise PackageError(f"Invalid {param_name}: {value}. Must be greater than {Package.MIN_DIMENSION}")
            
            if param_name == "mass":
                if value > Package.MAX_MASS:
                    raise PackageError(f"Mass exceeds maximum limit of {Package.MAX_MASS}kg")
            else:
                if value > Package.MAX_DIMENSION:
                    raise PackageError(f"Dimension exceeds maximum limit of {Package.MAX_DIMENSION}cm")
            
            return value
            
        except (ValueError, TypeError, InvalidOperation) as e:
            raise PackageError(f"Invalid {param_name}: {value}. Must be a valid number")
    
    @property
    def volume(self) -> float:
        """Calculate and cache the volume"""
        if self._volume is None:
            self._volume = self.width * self.height * self.length
        return self._volume
    
    @property
    def max_dimension(self) -> float:
        """Calculate and cache the maximum dimension"""
        if self._max_dimension is None:
            self._max_dimension = max(self.width, self.height, self.length)
        return self._max_dimension
    
    @property
    def is_bulky(self) -> bool:
        """Check if package is bulky"""
        return self.volume >= self.BULKY_VOLUME or self.max_dimension >= self.BULKY_DIMENSION
    
    @property
    def is_heavy(self) -> bool:
        """Check if package is heavy"""
        return self.mass >= self.HEAVY_MASS
    
    def get_stack(self) -> str:
        """Determine the appropriate stack for the package"""
        if self.is_bulky and self.is_heavy:
            return "REJECTED"
        elif self.is_bulky or self.is_heavy:
            return "SPECIAL"
        return "STANDARD"

def sort(width: Union[int, float, str], height: Union[int, float, str],
         length: Union[int, float, str], mass: Union[int, float, str]) -> str:
    """
    Sort packages into different stacks based on their dimensions and mass.
    
    Args:
        width: Width of the package in centimeters
        height: Height of the package in centimeters
        length: Length of the package in centimeters
        mass: Mass of the package in kilograms
    
    Returns:
        str: Stack designation ('STANDARD', 'SPECIAL', or 'REJECTED')
    
    Raises:
        PackageError: If any dimension or mass is invalid
    """
    package = Package(width, height, length, mass)
    return package.get_stack()
