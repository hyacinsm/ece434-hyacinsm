/**
 * @file   led.c
 * @author Sean Hyacinthe
 * @date   20 Jan 2024
 * @setup none needed, just compile 
 * @brief  Blinks two leds at two different rates uing mulithreading and kernel drivers
 * The sysfs entry appears at /sys/ebb/ledPair49_60
 * @see http://www.derekmolloy.ie/
*/

#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/gpio.h>       // Required for the GPIO functions
#include <linux/kobject.h>    // Using kobjects for the sysfs bindings
#include <linux/kthread.h>    // Using kthreads for the flashing functionality
#include <linux/delay.h>      // Using this header for the msleep() function

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Derek Molloy");
MODULE_DESCRIPTION("A simple Linux LED driver LKM for the BBB");
MODULE_VERSION("0.1");

static unsigned int gpioLED = 49;           ///< Default GPIO for the LED is 49
module_param(gpioLED, uint, S_IRUGO);       ///< Param desc. S_IRUGO can be read/not changed
MODULE_PARM_DESC(gpioLED, " GPIO LED number (default=49)");     ///< parameter description


static unsigned int gpioLED_2 = 60;           ///< Default GPIO for the LED is 49
module_param(gpioLED_2, uint, S_IRUGO);       ///< Param desc. S_IRUGO can be read/not changed
MODULE_PARM_DESC(gpioLED_2, " GPIO LED number (default=49)");     ///< parameter description


static unsigned int blinkPeriod = 1000;     ///< The blink period in ms
module_param(blinkPeriod, uint, S_IRUGO);   ///< Param desc. S_IRUGO can be read/not changed
MODULE_PARM_DESC(blinkPeriod, " LED blink period in ms (min=1, default=1000, max=10000)");

static unsigned int blinkPeriod_2 = 2000;     ///< The blink period in ms
module_param(blinkPeriod_2, uint, S_IRUGO);   ///< Param desc. S_IRUGO can be read/not changed
MODULE_PARM_DESC(blinkPeriod_2, " LED blink period 2 in ms (min=1, default=1000, max=10000)");

static char ledName[15] = "ledPairXXX_XXX";          ///< Null terminated default string -- just in case
static bool ledOn = 0;                      ///< Is the LED on or off? Used for flashing
static bool ledOn_2 = 0;
enum modes { OFF, ON, FLASH };              ///< The available LED modes -- static not useful here
static enum modes mode = FLASH;             ///< Default mode is flashing
static enum modes mode_2 = FLASH;

struct led_info {
   int *pin;
   int *period;
   bool *ledOn;
   enum modes *mode;

} led,led_2;


/** @brief A callback function to display the LED mode
 *  @param kobj represents a kernel object device that appears in the sysfs filesystem
 *  @param attr the pointer to the kobj_attribute struct
 *  @param buf the buffer to which to write the number of presses
 *  @return return the number of characters of the mode string successfully displayed
 */
static ssize_t mode_show(struct kobject *kobj, struct kobj_attribute *attr, char *buf){
   switch(mode){
      case OFF:   return sprintf(buf, "off\t");       // Display the state -- simplistic approach
      case ON:    return sprintf(buf, "on\t");
      case FLASH: return sprintf(buf, "flash\t");
      default:    return sprintf(buf, "LKM Error\t"); // Cannot get here
   }
}

/** @brief A callback function to store the LED mode using the enum above */
static ssize_t mode_store(struct kobject *kobj, struct kobj_attribute *attr, const char *buf, size_t count){
   // the count-1 is important as otherwise the \n is used in the comparison
   if (strncmp(buf,"on",count-1)==0) { mode = ON; }   // strncmp() compare with fixed number chars
   else if (strncmp(buf,"off",count-1)==0) { mode = OFF; }
   else if (strncmp(buf,"flash",count-1)==0) { mode = FLASH; }
   return count;
}


static ssize_t mode_show_2(struct kobject *kobj, struct kobj_attribute *attr, char *buf){
   switch(mode_2){
      case OFF:   return sprintf(buf, "off\t");       // Display the state -- simplistic approach
      case ON:    return sprintf(buf, "on\t");
      case FLASH: return sprintf(buf, "flash\t");
      default:    return sprintf(buf, "LKM Error\t"); // Cannot get here
   }
}

/** @brief A callback function to store the LED mode using the enum above */
static ssize_t mode_store_2(struct kobject *kobj, struct kobj_attribute *attr, const char *buf, size_t count){
   // the count-1 is important as otherwise the \n is used in the comparison
   if (strncmp(buf,"on",count-1)==0) { mode = ON; }   // strncmp() compare with fixed number chars
   else if (strncmp(buf,"off",count-1)==0) { mode = OFF; }
   else if (strncmp(buf,"flash",count-1)==0) { mode = FLASH; }
   return count;
}

/** @brief A callback function to display the LED period */
static ssize_t period_show(struct kobject *kobj, struct kobj_attribute *attr, char *buf){
   return sprintf(buf, "%d\\n", blinkPeriod);
}

/** @brief A callback function to store the LED period value */
static ssize_t period_store(struct kobject *kobj, struct kobj_attribute *attr, const char *buf, size_t count){
   unsigned int period;                     // Using a variable to validate the data sent
   sscanf(buf, "%du\n", &period);             // Read in the period as an unsigned int
   if ((period>1)&&(period<=10000)){        // Must be 2ms or greater, 10secs or less
      blinkPeriod = period;                 // Within range, assign to blinkPeriod variable
   }
   return period;
}


static ssize_t period_show_2(struct kobject *kobj, struct kobj_attribute *attr, char *buf){
   return sprintf(buf, "%d\n", blinkPeriod_2);
}

/** @brief A callback function to store the LED period value */
static ssize_t period_store_2(struct kobject *kobj, struct kobj_attribute *attr, const char *buf, size_t count){
   unsigned int period;                     // Using a variable to validate the data sent
   sscanf(buf, "%du\n", &period);             // Read in the period as an unsigned int
   if ((period>1)&&(period<=10000)){        // Must be 2ms or greater, 10secs or less
      blinkPeriod_2 = period;                 // Within range, assign to blinkPeriod variable
   }
   return period;
}

/** Use these helper macros to define the name and access levels of the kobj_attributes
 *  The kobj_attribute has an attribute attr (name and mode), show and store function pointers
 *  The period variable is associated with the blinkPeriod variable and it is to be exposed
 *  with mode 0666 using the period_show and period_store functions above
 */
static struct kobj_attribute period_attr = __ATTR(blinkPeriod, 0660, period_show, period_store);
static struct kobj_attribute period_attr_2 = __ATTR(blinkPeriod_2, 0660, period_show_2, period_store_2);

static struct kobj_attribute mode_attr = __ATTR(mode, 0660, mode_show, mode_store);
static struct kobj_attribute mode_attr_2 = __ATTR(mode_2, 0660, mode_show_2, mode_store_2);

/** The ebb_attrs[] is an array of attributes that is used to create the attribute group below.
 *  The attr property of the kobj_attribute is used to extract the attribute struct
 */
static struct attribute *ebb_attrs[] = {
   &period_attr.attr,                       // The period at which the LED flashes
   &period_attr_2.attr,
   &mode_attr.attr,                         // Is the LED on or off?
   &mode_attr_2.attr,
   NULL,
};

/** The attribute group uses the attribute array and a name, which is exposed on sysfs -- in this
 *  case it is gpio49, which is automatically defined in the ebbLED_init() function below
 *  using the custom kernel parameter that can be passed when the module is loaded.
 */
static struct attribute_group attr_group = {
   .name  = ledName,                        // The name is generated in ebbLED_init()
   .attrs = ebb_attrs,                      // The attributes array defined just above
};

static struct kobject *ebb_kobj;            /// The pointer to the kobject
static struct task_struct *task;            /// The pointer to the thread task
static struct task_struct *task_2;

/** @brief The LED Flasher main kthread loop
 *
 *  @param arg A void pointer used in order to pass data to the thread
 *  @return returns 0 if successful
 */
static int flash(void *arg){
   struct led_info *ptr = arg; 

   printk(KERN_INFO "EBB LED: Thread has started running \n");


   while(!kthread_should_stop()){           // Returns true when kthread_stop() is called
      set_current_state(TASK_RUNNING);
      if (*(ptr->mode)==FLASH) *(ptr->ledOn) = !(*(ptr->ledOn));      // Invert the LED state
      else if (*(ptr->mode)==ON) *(ptr->ledOn) = true;
      else *(ptr->ledOn) = false;
      gpio_set_value(*(ptr->pin), *(ptr->ledOn));       // Use the LED state to light/turn off the LED
      set_current_state(TASK_INTERRUPTIBLE);
      msleep(*(ptr->period)/2);                // millisecond sleep for half of the period
   }
   printk(KERN_INFO "EBB LED: Thread has run to completion \n");
   return 0;
}

/** @brief The LKM initialization function
 *  The static keyword restricts the visibility of the function to within this C file. The __init
 *  macro means that for a built-in driver (not a LKM) the function is only used at initialization
 *  time and that it can be discarded and its memory freed up after that point. In this example this
 *  function sets up the GPIOs and the IRQ
 *  @return returns 0 if successful
 */
static int __init ebbLED_init(void){
   int result = 0;
   void *led_flash_ptr = (void*) &led;
   void *led_2_flash_ptr = (void*) &led_2;

   led.pin = &gpioLED;
   led.period = &blinkPeriod;
   led.ledOn = &ledOn;
   led.mode = &mode;

   led_2.pin = &gpioLED_2;
   led_2.period = &blinkPeriod_2;
   led_2.ledOn = &ledOn_2;
   led_2.mode = &mode_2;

   


   printk(KERN_INFO "EBB LED: Initializing the EBB LED LKM\n");
   sprintf(ledName, "ledPair%d_%d", gpioLED,gpioLED_2);      // Create the gpio115 name for /sys/ebb/led49

   ebb_kobj = kobject_create_and_add("ebb", kernel_kobj->parent); // kernel_kobj points to /sys/kernel
   if(!ebb_kobj){
      printk(KERN_ALERT "EBB LED: failed to create kobject\n");
      return -ENOMEM;
   }
   // add the attributes to /sys/ebb/ -- for example, /sys/ebb/led49/ledOn
   result = sysfs_create_group(ebb_kobj, &attr_group);
   if(result) {
      printk(KERN_ALERT "EBB LED: failed to create sysfs group\n");
      kobject_put(ebb_kobj);                // clean up -- remove the kobject sysfs entry
      return result;
   }
   *led.ledOn = true;
   gpio_request(*led.pin, "sysfs");          // gpioLED is 49 by default, request it
   gpio_direction_output(*led.pin, *led.ledOn);   // Set the gpio to be in output mode and turn on
   gpio_export(*led.pin, false);  // causes gpio49 to appear in /sys/class/gpio
                                 // the second argument prevents the direction from being changed

   *led_2.ledOn = true;
   gpio_request(*led_2.pin , "sysfs");          // gpioLED is 49 by default, request it
   gpio_direction_output(*led_2.pin, *led_2.ledOn );   // Set the gpio to be in output mode and turn on
   gpio_export(*led_2.pin, false);  // causes gpio49 to appear in /sys/class/gpio

   task = kthread_run(flash, led_flash_ptr, "LED_flash_thread");  // Start the LED flashing thread
   task_2 = kthread_run(flash, led_2_flash_ptr , "LED_2_flash_thread");
   if(IS_ERR(task) || IS_ERR(task_2)){                                     // Kthread name is LED_flash_thread
      printk(KERN_ALERT "EBB LED: failed to create the task\n");
      return PTR_ERR(task);
   }
   return result;
}

/** @brief The LKM cleanup function
 *  Similar to the initialization function, it is static. The __exit macro notifies that if this
 *  code is used for a built-in driver (not a LKM) that this function is not required.
 */
static void __exit ebbLED_exit(void){
   kthread_stop(task);                      // Stop the LED flashing thread
   kobject_put(ebb_kobj);                   // clean up -- remove the kobject sysfs entry
   gpio_set_value(gpioLED, 0);              // Turn the LED off, indicates device was unloaded
   gpio_unexport(gpioLED);                  // Unexport the Button GPIO
   gpio_free(gpioLED);                      // Free the LED GPIO
   printk(KERN_INFO "EBB LED: Goodbye from the EBB LED LKM!\n");
}

/// This next calls are  mandatory -- they identify the initialization function
/// and the cleanup function (as above).
module_init(ebbLED_init);
module_exit(ebbLED_exit);
