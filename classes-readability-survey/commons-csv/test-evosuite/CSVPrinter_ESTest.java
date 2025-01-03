/*
 * This file was automatically generated by EvoSuite
 * Tue Apr 30 11:47:55 GMT 2024
 */

package org.apache.commons.csv;

import org.junit.Test;
import static org.junit.Assert.*;
import static org.evosuite.runtime.EvoAssertions.*;
import java.io.PipedWriter;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVPrinter;
import org.evosuite.runtime.EvoRunner;
import org.evosuite.runtime.EvoRunnerParameters;
import org.junit.runner.RunWith;

public class CSVPrinter_ESTest {

  @Test(timeout = 4000)
  public void test0()  throws Throwable  {
      PipedWriter pipedWriter0 = new PipedWriter();
      CSVPrinter cSVPrinter0 = null;
      try {
        cSVPrinter0 = new CSVPrinter(pipedWriter0, (CSVFormat) null);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // format
         //
         verifyException("java.util.Objects", e);
      }
  }
}
