package hackvent2018.evil;

import java.lang.reflect.Method;

public class Day18 {
  public static void main(String[] args) throws Exception {
    EvilLoader loader = new EvilLoader(Evilist.class.getClassLoader());
    
    Class evilEventClazz = loader.loadClass("hackvent2018.evil.EvilEvent");
    for (Method method : evilEventClazz.getDeclaredMethods()) {
        if (method.getName().contains("eventResult")) {
              method.setAccessible(true);
              String eventResult = (String) method.invoke(null);
              System.out.println(eventResult);
        }
    }
  }
}
