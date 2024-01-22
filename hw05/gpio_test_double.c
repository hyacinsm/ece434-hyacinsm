/**
 * @file   gpio_test_double.c
 * @author Derek Molloy & Sean Hyacinthe
 * @date    22 jan 2024
 * @brief  A kernel module for controlling a GPIO LED/button pair. The device mounts devices via
 * sysfs /sys/class/gpio/gpio48 and gpio50. 
 * @setup Therefore, this test LKM circuit assumes that an green LED
 * is attached to GPIO 48 which is on P9_14 and the button is attached to GPIO 50 on P9_15. In addtion,
 * it assumes there is a red LED connected to P8_15 and a push button connnect to P9_18
 * @see http://www.derekmolloy.ie/
*/

#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/gpio.h>                 // Required for the GPIO functions
#include <linux/interrupt.h>            // Required for the IRQ code

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Derek Molloy");
MODULE_DESCRIPTION("A Button/LED test driver for the BBB");
MODULE_VERSION("0.1");

static unsigned int greenLED = 60;       //P9_12 (GPIO60)
static unsigned int greenButton = 50;   ///P9_14 (GPIO50)

static unsigned int redLED = 47;       //P8_15 (GPIO47)
static unsigned int redButton = 65;   ///P9_18 (GPIO65)

static unsigned int greenIrqNumber;          ///< Used to share the IRQ number within this file
static unsigned int redIrqNumber;

static unsigned int numberPresses = 0;  ///< For information, store the number of button presses

static bool	    greenOn = 0;
static bool	    redOn = 0;            

/// Function prototype for the custom IRQ handler function -- see below for the implementation
static irq_handler_t  ebbgpio_green_irq_handler(unsigned int irq, void *dev_id, struct pt_regs *regs);
static irq_handler_t  ebbgpio_red_irq_handler(unsigned int irq, void *dev_id, struct pt_regs *regs);


/** @brief The LKM initialization function
 *  The static keyword restricts the visibility of the function to within this C file. The __init
 *  macro means that for a built-in driver (not a LKM) the function is only used at initialization
 *  time and that it can be discarded and its memory freed up after that point. In this example this
 *  function sets up the GPIOs and the IRQ
 *  @return returns 0 if successful
 */
static int __init ebbgpio_init(void){
   int greenResult = 0;
   int redResult = 0;
   printk(KERN_INFO "GPIO_TEST: Initializing the GPIO_TEST LKM\n");
   // Is the GPIO a valid GPIO number (e.g., the BBB has 4x32 but not all available)
   if (!gpio_is_valid(greenLED) || !gpio_is_valid(redLED)){
      printk(KERN_INFO "GPIO_TEST: invalid LED GPIO\n");
      return -ENODEV;
   }
   // Going to set up the LED. It is a GPIO in output mode and will be on by default
   greenOn = true;
   gpio_request(greenLED, "sysfs");          
   gpio_direction_output(greenLED, greenOn);   
   gpio_export(greenLED, false);             

   redOn = true;
   gpio_request(redLED, "sysfs");          
   gpio_direction_output(redLED, redOn);   
   gpio_export(redLED, false);  
		                  
   gpio_request(greenButton, "sysfs");       // Set up the greenButton
   gpio_direction_input(greenButton);        // Set the button GPIO to be an input
   gpio_set_debounce(greenButton, 200);      // Debounce the button with a delay of 200ms
   gpio_export(greenButton, false);          // Causes gpio115 to appear in /sys/class/gpio
			                    
   printk(KERN_INFO "GPIO_TEST: The Green button state =: %d\nGPIO_TEST: The Red button state =: %d\n", gpio_get_value(greenButton), gpio_get_value(redButton));

   greenIrqNumber = gpio_to_irq(greenButton);
   redIrqNumber = gpio_to_irq(redButton);

   printk(KERN_INFO "GPIO_TEST: The Green button is mapped to IRQ: %d\nPIO_TEST: The Red button is mapped to IRQ: %d\n", greenIrqNumber, redIrqNumber);

   greenResult = request_irq(greenIrqNumber,             // The interrupt number requested
                        (irq_handler_t) ebbgpio_green_irq_handler, // The pointer to the handler function below
                        IRQF_TRIGGER_RISING,   // Interrupt on rising edge (button press, not release)
                        "ebb_gpio_green_handler",    // Used in /proc/interrupts to identify the owner
                        NULL);                 // The *dev_id for shared interrupt lines, NULL is okay

   redResult = request_irq(redIrqNumber,             // The interrupt number requested
                        (irq_handler_t) ebbgpio_red_irq_handler, // The pointer to the handler function below
                        IRQF_TRIGGER_RISING,   // Interrupt on rising edge (button press, not release)
                        "ebb_gpio_red_handler",    // Used in /proc/interrupts to identify the owner
                        NULL);                 // The *dev_id for shared interrupt lines, NULL is okay

   printk(KERN_INFO "GPIO_TEST: The Green interrupt request result is: %d\nThe Red interrupt request result is: %d\n", greenResult, redResult);
   return greenResult & redResult;
}

/** @brief The LKM cleanup function
 *  Similar to the initialization function, it is static. The __exit macro notifies that if this
 *  code is used for a built-in driver (not a LKM) that this function is not required. Used to release the
 *  GPIOs and display cleanup messages.
 */
static void __exit ebbgpio_exit(void){
   printk(KERN_INFO "GPIO_TEST: The Green button state is currently: %d\nThe Red button state is currently: %d\n", gpio_get_value(greenButton), gpio_get_value(redButton));
   printk(KERN_INFO "GPIO_TEST: The button was pressed %d times\n", numberPresses);
   gpio_set_value(greenLED, 0);              
   gpio_unexport(greenLED);                  
   gpio_set_value(redLED, 0);             
   gpio_unexport(redLED);                  
   free_irq(greenIrqNumber, NULL);               
   free_irq(redIrqNumber, NULL);
   gpio_unexport(greenButton);               
   gpio_free(greenLED);                     
   gpio_free(greenButton); 
   gpio_unexport(redButton);               
   gpio_free(redLED);                     
   gpio_free(redButton);                    
   printk(KERN_INFO "GPIO_TEST: Goodbye from the LKM!\n");
}

/** @brief The GPIO IRQ Handler function
 *  This function is a custom interrupt handler that is attached to the GPIO above. The same interrupt
 *  handler cannot be invoked concurrently as the interrupt line is masked out until the function is complete.
 *  This function is static as it should not be invoked directly from outside of this file.
 *  @param irq    the IRQ number that is associated with the GPIO -- useful for logging.
 *  @param dev_id the *dev_id that is provided -- can be used to identify which device caused the interrupt
 *  Not used in this example as NULL is passed.
 *  @param regs   h/w specific register values -- only really ever used for debugging.
 *  return returns IRQ_HANDLED if successful -- should return IRQ_NONE otherwise.
 */
static irq_handler_t ebbgpio_green_irq_handler(unsigned int irq, void *dev_id, struct pt_regs *regs){
   greenOn = !greenOn;                          // Invert the LED state on each button press
   gpio_set_value(greenLED, greenOn);          // Set the physical LED accordingly
   printk(KERN_INFO "GPIO_TEST: Interrupt! (Green button state is %d)\n", gpio_get_value(greenButton));
   numberPresses++;                         // Global counter, will be outputted when the module is unloaded
   return (irq_handler_t) IRQ_HANDLED;      // Announce that the IRQ has been handled correctly
}

static irq_handler_t ebbgpio_red_irq_handler(unsigned int irq, void *dev_id, struct pt_regs *regs){
   redOn = !redOn;                          // Invert the LED state on each button press
   gpio_set_value(redLED, redOn);          // Set the physical LED accordingly
   printk(KERN_INFO "GPIO_TEST: Interrupt! (Red button state is %d)\n", gpio_get_value(redButton));
   numberPresses++;                         // Global counter, will be outputted when the module is unloaded
   return (irq_handler_t) IRQ_HANDLED;      // Announce that the IRQ has been handled correctly
}

/// This next calls are  mandatory -- they identify the initialization function
/// and the cleanup function (as above).
module_init(ebbgpio_init);
module_exit(ebbgpio_exit);
